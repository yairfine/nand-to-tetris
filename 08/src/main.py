import re
import sys
from pathlib import Path

VM_EXT = "*.vm"
ASM_EXT = ".asm"

RETURN_ADDRESS_COUNTER = 0


class Parser:
    GT_INSTRUCTION = "// gt\n(GT)\n@SP\nA=M-1\nA=A-1\nD=M\n@X_IS_POSITIVE_GT\nD;JGT\n@SP\nA=M-1\nD=M\n@NOT_GREATER_GT\nD;JGT\n@SP\nA=M-1\nD=-M\nA=A-1\nM=-M\nD=D-M\n@GREATER_GT\nD;JGT\n@NOT_GREATER_GT\n0;JMP\n(X_IS_POSITIVE_GT)\n@SP\nA=M-1\nD=M\n@GREATER_GT\nD;JLT\n(COMPARE_GREATER_GT)\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@GREATER_GT\nD;JGT\n(NOT_GREATER_GT)\n@SP\nM=M-1\nA=M-1\nM=0\n@AFTER_GREATER_GT\n0;JMP\n(GREATER_GT)\n@SP\nM=M-1\nA=M-1\nM=-1\n(AFTER_GREATER_GT)\n@R14\nA=M\n0;JMP"
    LT_INSTRUCTION = "// lt\n(LT)\n@SP\nA=M-1\nA=A-1\nD=M\n@X_IS_POSITIVE_LT\nD;JGT\n@SP\nA=M-1\nD=M\n@NOT_GREATER_LT\nD;JGT\n@SP\nA=M-1\nD=-M\nA=A-1\nM=-M\nD=D-M\n@GREATER_LT\nD;JGE\n@NOT_GREATER_LT\n0;JMP\n(X_IS_POSITIVE_LT)\n@SP\nA=M-1\nD=M\n@GREATER_LT\nD;JLT\n(COMPARE_GREATER_LT)\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@GREATER_LT\nD;JGE\n(NOT_GREATER_LT)\n@SP\nM=M-1\nA=M-1\nM=-1\n@AFTER_GREATER_LT\n0;JMP\n(GREATER_LT)\n@SP\nM=M-1\nA=M-1\nM=0\n(AFTER_GREATER_LT)\n@R14\nA=M\n0;JMP"
    EQ_INSTRUCTION = "// eq\n(EQ)\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@EQUALS\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@AFTER_EQUALS\n0;JMP\n(EQUALS)\n@SP\nM=M-1\nA=M-1\nM=-1\n(AFTER_EQUALS)\n@R14\nA=M\n0;JMP"

    def __init__(self, raw_data, filename):
        self.raw_data = raw_data
        self.filename = filename
        self.function_name = ""
        self.gt_return_flag = False
        self.lt_return_flag = False
        self.eq_return_flag = False

        self.convert_funcs = {"push": self.create_push_op,
                              "pop": self.create_pop_op,
                              "add": self.create_add_op,
                              "sub": self.create_sub_op,
                              "neg": self.create_neg_op,
                              "and": self.create_and_op,
                              "or": self.create_or_op,
                              "not": self.create_not_op,
                              "eq": self.create_eq_op,
                              "gt": self.create_gt_op,
                              "lt": self.create_lt_op,
                              "label": self.create_label_op,
                              "goto": self.create_goto_op,
                              "if-goto": self.create_if_goto_op,
                              "function": self.create_function_op,
                              "call": self.create_call_op,
                              "return": self.create_return_op}

        self.push_instructions = {
            "constant": "// push constant {i}\n@{i}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "argument": "// push argument {i}\n@ARG\nD=M\n@{i}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "local": "// push local {i}\n@LCL\nD=M\n@{i}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static": "// push static {i}\n@{filename}.{i}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "pointer": "// push pointer {i}\n@{this_or_that}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "temp": "// push temp {i}\n@{temp_pointer}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "this": "// push this {i}\n@THIS\nD=M\n@{i}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "that": "// push that {i}\n@THAT\nD=M\n@{i}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"}

        self.pop_instructions = {
            "argument": "// pop argument {i}\n@ARG\nD=M\n@{i}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n",
            "local": "// pop local {i}\n@LCL\nD=M\n@{i}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n",
            "static": "// pop static {i}\n@SP\nM=M-1\nA=M\nD=M\n@{filename}.{i}\nM=D\n",
            "pointer": "// pop pointer {i}\n@SP\nM=M-1\nA=M\nD=M\n@{this_or_that}\nM=D\n",
            "temp": "// pop temp {i}\n@SP\nM=M-1\nA=M\nD=M\n@{temp_pointer}\nM=D\n",
            "this": "// pop this {i}\n@THIS\nD=M\n@{i}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n",
            "that": "// pop that {i}\n@THAT\nD=M\n@{i}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n"}

        self.pointer_route = {"0": "THIS", "1": "THAT"}

        self.ADD_INSTRUCTION = "// add\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=M+D\n@SP\nM=M-1\n"
        self.SUB_INSTRUCTION = "// sub\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=M-D\n@SP\nM=M-1\n"
        self.NEG_INSTRUCTION = "// neg\n@SP\nA=M-1\nM=-M\n"
        self.AND_INSTRUCTION = "// and\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=D&M\n@SP\nM=M-1\n"
        self.OR_INSTRUCTION = "// or\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=D|M\n@SP\nM=M-1\n"
        self.NOT_INSTRUCTION = "// not\n@SP\nA=M-1\nM=!M\n"
        self.EQ_GOTO = "// eq goto\n@eq_return_lbl_{0}\nD=A\n@R14\nM=D\n@EQ\n0;JMP\n(eq_return_lbl_{0})\n"
        self.GT_GOTO = "// gt goto\n@gt_return_lbl_{0}\nD=A\n@R14\nM=D\n@GT\n0;JMP\n(gt_return_lbl_{0})\n"
        self.LT_GOTO = "// lt goto\n@lt_return_lbl_{0}\nD=A\n@R14\nM=D\n@LT\n0;JMP\n(lt_return_lbl_{0})\n"
        self.PUSH_RETURN_ADDRESS = "// push return address\n@{function_name}$ret.{return_address_counter}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.LABEL_INSTRUCTION = "// label\n({function_name}${label_name})\n"
        self.GOTO_INSTRUCTION = "// goto {function_name}${label_name}\n@{function_name}${label_name}\n0;JMP\n"
        self.IF_GOTO_INSTRUCTION = "// if-goto {function_name}${label_name}\n@SP\nM=M-1\nA=M\nD=M\n@{function_name}${label_name}\nD;JNE\n"
        self.CALL_INSTRUCTION = "// call {function_name}\n// push LCL of the caller\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n// push ARG of the caller\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n// push THIS of the caller\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n// push THAT of the caller\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n// repositions ARG\n@{args_pos}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n// repositions LCL\n@SP\nD=M\n@LCL\nM=D\n@{function_name}\n0;JMP\n"
        self.RETURN_INSTRUCTION = "// return\n// endFrame = LCL\n@LCL\nD=M\n@R13 // endFrame\nM=D\n// retAddr = *(endFrame - 5)\n@LCL\nD=M-1\nD=D-1\nD=D-1\nD=D-1\nA=D-1\nD=M\n@R14 // retAddr\nM=D\n// *ARG = pop()\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n// SP = ARG + 1\n@ARG\nD=M\n@SP\nM=D+1\n// THAT = *(endFrame - 1)\n@R13\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n// THIS = *(endFrame - 2)\n@R13\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n// ARG = *(endFrame - 3)\n@R13\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n// LCL = *(endFrame - 4)\n@R13\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n// goto retAddr\n@R14\nA=M\n0;JMP\n"
        self.BOOTSTRAP_INSTRUCTION = "// bootstrap\n@256\nD=A\n@SP\nM=D\n"

    def parse(self):
        clean_data = self.preprocessor()
        result = ""
        for line in clean_data:
            op_type, *args = line.split(" ")

            func = self.convert_funcs[op_type]
            asm_commands = func(*args)
            result += asm_commands

        return result

    def preprocessor(self):
        clean_data = []

        for line in self.raw_data:
            line = line.rstrip("\n\r")

            if re.search("^\s*$", line) or line.startswith('//'):
                continue

            else:
                no_comments_line = re.sub('\s+(//).+', "", line)
                formated_line = re.sub('[ ]+', " ", no_comments_line)
                clean_line = formated_line.strip(" ")
                clean_data.append(clean_line)

        return clean_data

    def create_push_op(self, segment, i):
        this_or_that = self.pointer_route.get(i, "")
        temp_pointer = int(i) + 5
        instructions = self.push_instructions[segment]
        formatted_instructions = instructions.format(i=i,
                                                     filename=self.filename,
                                                     this_or_that=this_or_that,
                                                     temp_pointer=temp_pointer)
        return formatted_instructions

    def create_pop_op(self, segment, i):
        this_or_that = self.pointer_route.get(i, "")
        temp_pointer = int(i) + 5
        instructions = self.pop_instructions[segment]
        formatted_instructions = instructions.format(i=i,
                                                     filename=self.filename,
                                                     this_or_that=this_or_that,
                                                     temp_pointer=temp_pointer)
        return formatted_instructions

    def create_add_op(self):
        return self.ADD_INSTRUCTION

    def create_sub_op(self):
        return self.SUB_INSTRUCTION

    def create_neg_op(self):
        return self.NEG_INSTRUCTION

    def create_and_op(self):
        return self.AND_INSTRUCTION

    def create_or_op(self):
        return self.OR_INSTRUCTION

    def create_not_op(self):
        return self.NOT_INSTRUCTION

    def create_eq_op(self):
        global RETURN_ADDRESS_COUNTER
        RETURN_ADDRESS_COUNTER += 1
        op_codes = self.EQ_GOTO.format(RETURN_ADDRESS_COUNTER)
        self.eq_return_flag = True
        return op_codes

    def create_gt_op(self):
        global RETURN_ADDRESS_COUNTER

        RETURN_ADDRESS_COUNTER += 1
        op_codes = self.GT_GOTO.format(RETURN_ADDRESS_COUNTER)
        self.gt_return_flag = True

        return op_codes

    def create_lt_op(self):
        global RETURN_ADDRESS_COUNTER

        RETURN_ADDRESS_COUNTER += 1
        op_codes = self.LT_GOTO.format(RETURN_ADDRESS_COUNTER)
        self.lt_return_flag = True
        return op_codes

    def push_return_address(self):
        global RETURN_ADDRESS_COUNTER

        RETURN_ADDRESS_COUNTER += 1
        return self.PUSH_RETURN_ADDRESS.format(function_name=self.function_name,
                                               return_address_counter=RETURN_ADDRESS_COUNTER)

    def declare_return_address_label(self):
        global RETURN_ADDRESS_COUNTER

        return "({function_name}$ret.{return_address_counter})\n".format(
            function_name=self.function_name,
            return_address_counter=RETURN_ADDRESS_COUNTER)

    def create_label_op(self, label_name):
        return self.LABEL_INSTRUCTION.format(function_name=self.function_name,
                                             label_name=label_name)

    def create_goto_op(self, label_name):
        return self.GOTO_INSTRUCTION.format(function_name=self.function_name,
                                            label_name=label_name)

    def create_if_goto_op(self, label_name):
        return self.IF_GOTO_INSTRUCTION.format(function_name=self.function_name,
                                               label_name=label_name)

    def create_function_op(self, function_name, nVars):
        self.function_name = function_name
        op_codes = "// function {0}\n({0})\n".format(function_name)

        for i in range(int(nVars)):
            op_codes += self.create_push_op("constant", "0")

        return op_codes

    def create_call_op(self, function_name, nArgs):
        op_code = self.push_return_address()
        args_pos = int(nArgs) + 5
        op_code += self.CALL_INSTRUCTION.format(function_name=function_name,
                                                args_pos=args_pos)
        op_code += self.declare_return_address_label()
        return op_code

    def create_return_op(self):
        return self.RETURN_INSTRUCTION

    def create_bootstrap(self):
        bootstrap = self.BOOTSTRAP_INSTRUCTION
        bootstrap += self.create_call_op("Sys.init", 0)
        return bootstrap


class VMTranslator:
    def __init__(self):
        self._input_arg = self._parse_args()

    def _parse_args(self):
        return sys.argv[1]

    def _write_file(self, filename, binary_code):
        with filename.open("w") as fh:
            fh.write(binary_code)

    def _glob(self):
        files = []

        input_path = Path(self._input_arg)
        if input_path.is_dir():
            output_path = (input_path / input_path.name).with_suffix(ASM_EXT)
            for file in input_path.glob(VM_EXT):
                files.append(file)

        else:
            output_path = input_path.with_suffix(ASM_EXT)
            files.append(input_path)

        return files, output_path

    def run(self):
        should_add_gt = False
        should_add_lt = False
        should_add_eq = False

        parser = Parser("", "")
        parser.function_name = "Bootstrap"

        binary_code = parser.create_bootstrap()

        files, output_path = self._glob()
        for file in files:
            with file.open("r") as fh:
                lines = fh.readlines()
            parser = Parser(lines, file.stem)
            binary_code += parser.parse()

            if parser.lt_return_flag:
                should_add_lt = True
            if parser.gt_return_flag:
                should_add_gt = True
            if parser.eq_return_flag:
                should_add_eq = True

        if should_add_gt:
            binary_code += parser.GT_INSTRUCTION
        if should_add_lt:
            binary_code += parser.LT_INSTRUCTION
        if should_add_eq:
            binary_code += parser.EQ_INSTRUCTION

        self._write_file(output_path, binary_code)


if __name__ == '__main__':
    translator = VMTranslator()
    translator.run()
