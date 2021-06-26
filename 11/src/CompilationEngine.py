from JackTokenizer import TokenType
from SymbolTable import SymbolTable, FIELD_KIND

CONSTRUCTOR_FUNC = "constructor"
STATIC_FUNC = "function"
METHOD_FUNC = "method"
ARITHMETIC_OPERATORS = ("+", "-", "*", "/", "&", "|", "<", ">", "=")

class CompilationEngine:
    def __init__(self, tokenizer, vm_writer):
        self.tokenizer = tokenizer
        self.vm_writer = vm_writer
        self.symbol_table = SymbolTable()
        self.statement_func = {
            "let": self.compileLet,
            "if": self.compileIf,
            "while": self.compile_while,
            "do": self.compile_do,
            "return": self.compile_return
        }

        self.class_name = None
        self.label_counter = 0
        self.subroutine_type = None
        self.return_type = None


    def _generate_label(self, prefix="L"):
        label = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return label

    def _eat(self, token=None):
        if isinstance(token, str) and self.tokenizer.get_value() != token:
            return None
        elif isinstance(token, list) and self.tokenizer.get_value() not in token:
            return None

        eaten = self.tokenizer.get_value()
        self.tokenizer.advance()
        return eaten

    def compile_class(self):
        """
        Convert a Class implementation to VM instructions.
        """
        self._eat("class")
        self.class_name = self._eat()
        self._eat("{")

        while self.tokenizer.tokenType() == TokenType.keyword and (
                self.tokenizer.get_value() == "static" or self.tokenizer.get_value() == "field"):
            self.compileClassVarDec()

        while self.tokenizer.get_value() in (CONSTRUCTOR_FUNC, STATIC_FUNC, METHOD_FUNC):
            self.compile_subroutine_dec()

        self._eat("}")

        return

    def compileClassVarDec(self):
        kind = self._eat()
        type = self._eat()
        name = self._eat()
        self.symbol_table.define(name, type, kind)

        while self._eat(","):
            name = self._eat()
            self.symbol_table.define(name, type, kind)

        self._eat(";")

    def _add_constructor_memory_alloc(self):
        n_fields = self.symbol_table.varCount(FIELD_KIND)
        self.vm_writer.write_push("constant", n_fields)
        self.vm_writer.write_call("Memory.alloc", 1)
        self.vm_writer.write_pop("pointer", 0)

    def compile_subroutine_dec(self):
        self.symbol_table.start_subroutine()
        self.subroutine_type = self._eat([CONSTRUCTOR_FUNC, STATIC_FUNC, METHOD_FUNC])

        if self.subroutine_type == METHOD_FUNC:
            self.symbol_table.define("this", self.class_name, "arg")

        self.return_type = self._eat()
        function_name = self._eat()

        self._eat("(")
        self.compileParameterList()
        self._eat(")")
        self._eat("{")
        nVars = self.compileSubroutineBodyVarDecs()

        self.vm_writer.write_function(f"{self.class_name}.{function_name}", nVars)

        if self.subroutine_type == CONSTRUCTOR_FUNC:
            self._add_constructor_memory_alloc()
        elif self.subroutine_type == METHOD_FUNC:
            self.vm_writer.write_push("arg", 0)
            self.vm_writer.write_pop("pointer", 0)

        self.compileStatements()

        self._eat("}")

    def compileParameterList(self):
        """
        Update Symbol Table with the subroutine parameters.
        """
        while not self._eat(")"):
            type = self._eat()
            name = self._eat()
            self.symbol_table.define(name, type, "arg")
            self._eat(",")

    def compileSubroutineBodyVarDecs(self):
        nVars = 0
        while self.tokenizer.get_value() == "var":
            nVars += self.compileVarDec()

        return nVars

    def compileVarDec(self):
        n_locals = 0

        kind = self._eat("var")
        type = self._eat()
        name = self._eat()
        self.symbol_table.define(name, type, kind)
        n_locals += 1

        while self._eat(","):
            name = self._eat()
            self.symbol_table.define(name, type, kind)
            n_locals += 1

        self._eat(";")

        return n_locals

    def compileStatements(self):
        while self.tokenizer.get_value() != "}":
            statement_func = self.statement_func[self.tokenizer.get_value()]
            statement_func()

    def compileLet(self):
        """
        letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        """
        is_array = False
        self._eat("let")

        name = self._eat()

        if self.tokenizer.get_value() == "[":
            is_array = True
            self._compile_array_index(name)

        self._eat("=")
        self.compileExpression()
        self._eat(";")

        if is_array:
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)

        else:
            self.vm_writer.write_pop(self.symbol_table.kindOf(name),
                                     self.symbol_table.indexOf(name))

    def compileIf(self):
        """
        ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        true_label = self._generate_label("IF_TRUE")
        false_label = self._generate_label("IF_FALSE")
        exit_label = self._generate_label("IF_END")

        self._eat("if")
        self._eat("(")
        self.compileExpression()
        self._eat(")")

        self.vm_writer.write_if(true_label)
        self.vm_writer.write_goto(false_label)

        self.vm_writer.write_label(true_label)
        self._eat("{")
        self.compileStatements()
        self._eat("}")

        if self.tokenizer.get_value() == "else":
            self.vm_writer.write_goto(exit_label)

        self.vm_writer.write_label(false_label)

        if self._eat("else"):
            self._eat("{")
            self.compileStatements()
            self._eat("}")
            self.vm_writer.write_label(exit_label)


    def compile_while(self):
        """
        whileStatement: 'while' ( 'expression' ) '{' statements '}'
        """
        loop_label = self._generate_label()
        break_label = self._generate_label()

        self.vm_writer.write_label(loop_label)
        self._eat("while")
        self._eat("(")
        self.compileExpression()
        self._eat(")")
        self.vm_writer.write_arithmetic("not")

        self.vm_writer.write_if(break_label)
        self._eat("{")
        self.compileStatements()
        self._eat("}")
        self.vm_writer.write_goto(loop_label)

        self.vm_writer.write_label(break_label)

    def compile_do(self):
        """
        doStatement: 'do' subroutineCall ';'
        """
        self._eat("do")
        self.compileSubroutineCall()
        self.vm_writer.write_pop("temp", 0)
        self._eat(";")

    def compile_return(self):
        """
        returnStatement: 'return' expression? ';'
        """
        self._eat("return")

        if self.subroutine_type == CONSTRUCTOR_FUNC and self._eat("this"):
            self.vm_writer.write_push("pointer", 0)

        elif self.return_type == "void":
            self.vm_writer.write_push("constant", 0)

        else:
            if not self._eat(";"):
                self.compileExpression()

        self._eat(";")
        self.vm_writer.write_return()

    def compileSubroutineCall(self):
        function_name = self._eat()
        num_of_args = 0

        if self._eat("."):
            kind = self.symbol_table.kindOf(function_name)
            index = self.symbol_table.indexOf(function_name)
            if kind is not None:
                self.vm_writer.write_push(kind, index)
                function_name = self.symbol_table.typeOf(function_name) + "." + self._eat()
                num_of_args += 1
            else:
                function_name += "."
                function_name += self._eat()
        else:
            self.vm_writer.write_push("pointer", 0)
            function_name = self.class_name + "." + function_name
            num_of_args += 1

        self._eat("(")
        num_of_args += self.compileExpressionList()
        self._eat(")")
        self.vm_writer.write_call(function_name, num_of_args)

    def _compile_array_index(self, name):
        self.vm_writer.write_push(self.symbol_table.kindOf(name),
                                  self.symbol_table.indexOf(name))

        self._eat("[")
        self.compileExpression()
        self._eat("]")

        self.vm_writer.write_arithmetic("add")

    def compileTerm(self):
        """
         integerConstant | stringConstant | keywordConstant | varName | varName '['expression']' | subroutineCall | '(' expression ')' | unaryOp term
        """
        # Unary operator expression
        if self._eat("-"):
            self.compileTerm()
            self.vm_writer.write_arithmetic("neg")
            return
        elif self._eat("~"):
            self.compileTerm()
            self.vm_writer.write_arithmetic("not")
            return

        # An expression encapsulated inside parenthesis.
        if self._eat("("):
            self.compileExpression()
            self._eat(")")
            return

        # Calling subroutine of current class, or different class.
        if self.tokenizer.previewNext() == "(" or self.tokenizer.previewNext() == ".":
            self.compileSubroutineCall()
            return

        term = self._eat()

        if self.tokenizer.get_value() == "[":
            self._compile_array_index(term)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("that", 0)
        else:
            if term.isdecimal():
                self.vm_writer.write_push("constant", int(term))
            elif term == "true":
                self.vm_writer.write_push("constant", 0)
                self.vm_writer.write_arithmetic("not")
            elif term == "false":
                self.vm_writer.write_push("constant", 0)
            elif term == "null":
                self.vm_writer.write_push("constant", 0)
            elif term.startswith('"') and term.endswith('"'):
                term = term.strip('"')
                string_length = len(term)
                self.vm_writer.write_push("constant", string_length)
                self.vm_writer.write_call("String.new", 1)
                for char in term:
                    self.vm_writer.write_push("constant", ord(char))
                    self.vm_writer.write_call("String.appendChar", 2)
            else:
                self.vm_writer.write_push(self.symbol_table.kindOf(term),
                                          self.symbol_table.indexOf(term))


    def compileExpression(self):
        self.compileTerm()

        operators = []
        while self.tokenizer.get_value() in ARITHMETIC_OPERATORS:
            operators.append(self._eat())
            self.compileTerm()

            # If there is a saved operator, pop it in a FIFO manner
            # and write the matching VM instruction.
            if operators:
                self.vm_writer.write_arithmetic(operators.pop(0))

    def compileExpressionList(self):
        count = 0
        while self.tokenizer.get_value() != ")":
            self.compileExpression()
            self._eat(",")
            count += 1

        return count