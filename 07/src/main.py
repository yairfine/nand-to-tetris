import re
import sys
from pathlib import Path

VM_EXT = "*.vm"
ASM_EXT = ".asm"


class Parser:
    def __init__(self, raw_data, filename):
        self.raw_data = raw_data
        self.filename = filename
        self.return_address_counter = 0
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
                              "lt": self.create_lt_op}

        self.push_instructions = {
            "constant": "// push constant {0}\n@{0}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "argument": "// push argument {0}\n@ARG\nD=M\n@{0}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "local": "// push local {0}\n@LCL\nD=M\n@{0}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static": "// push static {0}\n@{1}.{0}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "pointer": "// push pointer {0}\n@{2}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "temp": "// push temp {0}\n@{3}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "this": "// push this {0}\n@THIS\nD=M\n@{0}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "that": "// push that {0}\n@THAT\nD=M\n@{0}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"}

        self.pop_instructions = {
            "argument": "// pop argument {0}\n@ARG\nD=M\n@{0}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n",
            "local": "// pop local {0}\n@LCL\nD=M\n@{0}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n",
            "static": "// pop static {0}\n@SP\nM=M-1\nA=M\nD=M\n@{1}.{0}\nM=D\n",
            "pointer": "// pop pointer {0}\n@SP\nM=M-1\nA=M\nD=M\n@{2}\nM=D\n",
            "temp": "// pop temp {0}\n@SP\nM=M-1\nA=M\nD=M\n@{3}\nM=D\n",
            "this": "// pop this {0}\n@THIS\nD=M\n@{0}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n",
            "that": "// pop that {0}\n@THAT\nD=M\n@{0}\nD=D+A\n@SP\nA=M\nM=D\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1\n"}

        self.pointer_route = {"0": "THIS", "1": "THAT"}

        self.ADD_INSTRUCTION = "// add\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=M+D\n@SP\nM=M-1\n"
        self.SUB_INSTRUCTION = "// sub\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=M-D\n@SP\nM=M-1\n"
        self.NEG_INSTRUCTION = "// neg\n@SP\nA=M-1\nM=-M\n"
        self.AND_INSTRUCTION = "// and\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=D&M\n@SP\nM=M-1\n"
        self.OR_INSTRUCTION = "// or\n@SP\nA=M-1\nD=M\n@SP\nA=M-1\nA=A-1\nM=D|M\n@SP\nM=M-1\n"
        self.NOT_INSTRUCTION = "// not\n@SP\nA=M-1\nM=!M\n"
        self.EQ_INSTRUCTION = "// eq\n(EQ)\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@EQUALS\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@AFTER_EQUALS\n0;JMP\n(EQUALS)\n@SP\nM=M-1\nA=M-1\nM=-1\n(AFTER_EQUALS)\n@SP\nA=M+1\nA=M\n0;JMP\n"
        self.EQ_GOTO = "// eq goto\n@EQ\n0;JMP\n"
        self.GT_INSTRUCTION = "// gt\n(GT)\n@SP\nA=M-1\nA=A-1\nD=M\n@X_IS_POSITIVE_GT\nD;JGT\n@SP\nA=M-1\nD=M\n@NOT_GREATER_GT\nD;JGT\n@SP\nA=M-1\nD=-M\nA=A-1\nM=-M\nD=D-M\n@GREATER_GT\nD;JGT\n@NOT_GREATER_GT\n0;JMP\n(X_IS_POSITIVE_GT)\n@SP\nA=M-1\nD=M\n@GREATER_GT\nD;JLT\n(COMPARE_GREATER_GT)\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@GREATER_GT\nD;JGT\n(NOT_GREATER_GT)\n@SP\nM=M-1\nA=M-1\nM=0\n@AFTER_GREATER_GT\n0;JMP\n(GREATER_GT)\n@SP\nM=M-1\nA=M-1\nM=-1\n(AFTER_GREATER_GT)\n@SP\nA=M+1\nA=M\n0;JMP\n"
        self.GT_GOTO = "// gt goto\n@GT\n0;JMP\n"
        self.LT_INSTRUCTION = "// lt\n(LT)\n@SP\nA=M-1\nA=A-1\nD=M\n@X_IS_POSITIVE_LT\nD;JGT\n@SP\nA=M-1\nD=M\n@NOT_GREATER_LT\nD;JGT\n@SP\nA=M-1\nD=-M\nA=A-1\nM=-M\nD=D-M\n@GREATER_LT\nD;JGE\n@NOT_GREATER_LT\n0;JMP\n(X_IS_POSITIVE_LT)\n@SP\nA=M-1\nD=M\n@GREATER_LT\nD;JLT\n(COMPARE_GREATER_LT)\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@GREATER_LT\nD;JGE\n(NOT_GREATER_LT)\n@SP\nM=M-1\nA=M-1\nM=-1\n@AFTER_GREATER_LT\n0;JMP\n(GREATER_LT)\n@SP\nM=M-1\nA=M-1\nM=0\n(AFTER_GREATER_LT)\n@SP\nA=M+1\nA=M\n0;JMP\n"
        self.LT_GOTO = "// lt goto\n@LT\n0;JMP\n"
        self.LOAD_RETURN_ADDRESS = "// return address\n@RETURN_ADDRESS_{}\nD=A\n@SP\nA=M\nM=D\n"

    def parse(self):
        result = ""
        clean_data = self.preprocessor()
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
                clean_line = re.sub('\s+', "", no_comments_line)
                clean_data.append(clean_line)

        return clean_data

    def create_push_op(self, segment, i):
        this_or_that = self.pointer_route.get(i, "")
        temp_pointer = int(i) + 5
        instructions = self.push_instructions[segment]
        formatted_instructions = instructions.format(i, self.filename,
                                                     this_or_that,
                                                     temp_pointer)
        return formatted_instructions

    def create_pop_op(self, segment, i):
        this_or_that = self.pointer_route.get(i, "")
        temp_pointer = int(i) + 5
        instructions = self.pop_instructions[segment]
        formatted_instructions = instructions.format(i, self.filename,
                                                     this_or_that,
                                                     temp_pointer)
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
        op_codes = self.load_return_address()

        if not self.eq_return_flag:
            op_codes += self.EQ_INSTRUCTION
            self.eq_return_flag = True

        else:
            op_codes += self.EQ_GOTO

        op_codes += self.create_return_address_label()

        return op_codes

    def create_gt_op(self):
        op_codes = self.load_return_address()

        if not self.gt_return_flag:
            op_codes += self.GT_INSTRUCTION
            self.gt_return_flag = True

        else:
            op_codes += self.GT_GOTO

        op_codes += self.create_return_address_label()

        return op_codes

    def create_lt_op(self):
        op_codes = self.load_return_address()

        if not self.lt_return_flag:
            op_codes += self.LT_INSTRUCTION
            self.lt_return_flag = True

        else:
            op_codes += self.LT_GOTO

        op_codes += self.create_return_address_label()

        return op_codes

    def load_return_address(self):
        self.return_address_counter += 1
        return self.LOAD_RETURN_ADDRESS.format(self.return_address_counter)

    def create_return_address_label(self):
        return "(RETURN_ADDRESS_{})\n".format(self.return_address_counter)


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
        binary_code = ""

        files, output_path = self._glob()
        for file in files:
            with file.open("r") as fh:
                lines = fh.readlines()
            parser = Parser(lines, file.stem)
            binary_code += parser.parse()

        self._write_file(output_path, binary_code)


if __name__ == '__main__':
    translator = VMTranslator()
    translator.run()
