import xml.etree.ElementTree as ElementTree
from xml.dom import minidom
from JackTokenizer import TokenType


class CompilationEngine:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.statement_func = {
            "let": self.compileLet,
            "if": self.compileIf,
            "while": self.compileWhile,
            "do": self.compileDo,
            "return": self.compileReturn
        }

    def eat(self, parent, token=None):

        if isinstance(token, str) and self.tokenizer.get_value() != token:
            return False
        elif isinstance(token, list) and self.tokenizer.get_value() not in token:
            return False

        token_type = self.tokenizer.tokenType()

        element = ElementTree.SubElement(parent, token_type.name)

        element.text = self.tokenizer.get_value()
        self.tokenizer.advance()
        return True

    def fix(self, xml_output):
        xml_output = xml_output.replace("<parameterList/>", "<parameterList>\n</parameterList>")
        xml_output = xml_output.replace("<expressionList/>", "<expressionList>\n</expressionList>")
        xml_output = xml_output.replace("<statements/>", "<statements>\n</statements>")

        return xml_output

    def compileClass(self):
        root = ElementTree.Element("class")

        self.eat(root)
        self.eat(root)
        self.eat(root, "{")

        while self.tokenizer.tokenType() == TokenType.keyword and (
                self.tokenizer.keyword() == "static" or self.tokenizer.keyword() == "field"):
            self.compileClassVarDec(root)

        while self.tokenizer.get_value() in ["constructor", "function", "method"]:
            self.compileSubroutineDec(root)

        self.eat(root, "}")

        rough_string = ElementTree.tostring(root, encoding="utf-8", short_empty_elements=False)
        reparsed = minidom.parseString(rough_string)
        xml_output = reparsed.toprettyxml(indent="  ")
        xml_output = self.fix(xml_output)
        return xml_output

        # return ElementTree.tostring(root, encoding="utf-8", method="xml")

        # document = ElementTree.ElementTree(root)
        # document.write("temp.xml", encoding="utf-8", xml_declaration=False, short_empty_elements=False)

        # return ElementTree.ElementTree(root)

    def compileClassVarDec(self, parent):
        fieldDecTag = ElementTree.SubElement(parent, "classVarDec")

        while not self.eat(fieldDecTag, ";"):
            self.eat(fieldDecTag)

    def compileSubroutineDec(self, parent):
        subroutineDecTag = ElementTree.SubElement(parent, "subroutineDec")

        self.eat(subroutineDecTag, ["constructor", "function", "method"])
        self.eat(subroutineDecTag)
        self.eat(subroutineDecTag)
        self.eat(subroutineDecTag, "(")
        self.compileParameterList(subroutineDecTag)
        self.eat(subroutineDecTag, ")")
        self.compileSubroutineBody(subroutineDecTag)

    def compileParameterList(self, parent):
        parameterListTag = ElementTree.SubElement(parent, "parameterList")

        while self.tokenizer.get_value() != ")":
            self.eat(parameterListTag)

    def compileSubroutineBody(self, parent):
        subroutineBodyTag = ElementTree.SubElement(parent, "subroutineBody")

        self.eat(subroutineBodyTag, "{")

        while self.tokenizer.get_value() == "var":
            self.compileVarDec(subroutineBodyTag)

        self.compileStatements(subroutineBodyTag)

        self.eat(subroutineBodyTag, "}")

    def compileVarDec(self, parent):
        varDecTag = ElementTree.SubElement(parent, "varDec")

        while not self.eat(varDecTag, ";"):
            self.eat(varDecTag)

    def compileStatements(self, parent):
        statementsTag = ElementTree.SubElement(parent, "statements")

        while self.tokenizer.get_value() != "}":
            statement_func = self.statement_func[self.tokenizer.get_value()]
            statement_func(statementsTag)

    def compileLet(self, parent):
        let_statement = ElementTree.SubElement(parent, "letStatement")

        self.eat(let_statement, "let")
        self.eat(let_statement)

        if self.tokenizer.get_value() == "[":
            self.eat(let_statement, "[")
            self.compileExpression(let_statement)
            self.eat(let_statement, "]")

        self.eat(let_statement, "=")
        self.compileExpression(let_statement)
        self.eat(let_statement, ";")

    def compileIf(self, parent):
        if_statement = ElementTree.SubElement(parent, "ifStatement")

        self.eat(if_statement, "if")
        self.eat(if_statement, "(")
        self.compileExpression(if_statement)
        self.eat(if_statement, ")")
        self.eat(if_statement, "{")
        self.compileStatements(if_statement)
        self.eat(if_statement, "}")

        if self.eat(if_statement, "else"):
            self.eat(if_statement, "{")
            self.compileStatements(if_statement)
            self.eat(if_statement, "}")

    def compileWhile(self, parent):
        while_statement = ElementTree.SubElement(parent, "whileStatement")

        self.eat(while_statement, "while")
        self.eat(while_statement, "(")
        self.compileExpression(while_statement)
        self.eat(while_statement, ")")
        self.eat(while_statement, "{")
        self.compileStatements(while_statement)
        self.eat(while_statement, "}")

    def compileDo(self, parent):
        do_statement = ElementTree.SubElement(parent, "doStatement")

        self.eat(do_statement, "do")
        self.compileSubroutineCall(do_statement)
        self.eat(do_statement, ";")

    def compileReturn(self, parent):
        return_statement = ElementTree.SubElement(parent, "returnStatement")

        self.eat(return_statement, "return")

        if not self.eat(return_statement, ";"):
            self.compileExpression(return_statement)
            self.eat(return_statement, ";")

    def compileTerm(self, parent):
        term_tag = ElementTree.SubElement(parent, "term")

        if self.eat(term_tag, "-") or self.eat(term_tag, "~"):
            self.compileTerm(term_tag)
            return

        if self.eat(term_tag, "("):
            self.compileExpression(term_tag)
            self.eat(term_tag, ")")
            return

        if self.tokenizer.previewNext() == "(" or self.tokenizer.previewNext() == ".":
            self.compileSubroutineCall(term_tag)
            return

        self.eat(term_tag)

        if self.eat(term_tag, "["):
            self.compileExpression(term_tag)
            self.eat(term_tag, "]")

    def compileExpression(self, parent):
        expression_tag = ElementTree.SubElement(parent, "expression")

        self.compileTerm(expression_tag)

        while self.tokenizer.get_value() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.eat(expression_tag)
            self.compileTerm(expression_tag)

        return

    def compileExpressionList(self, parent):
        expression_list = ElementTree.SubElement(parent, "expressionList")

        while self.tokenizer.get_value() != ")":
            self.compileExpression(expression_list)
            self.eat(expression_list, ",")

    def compileSubroutineCall(self, parent):
        self.eat(parent)
        if self.eat(parent, "."):
            self.eat(parent)

        self.eat(parent, "(")
        self.compileExpressionList(parent)
        self.eat(parent, ")")
