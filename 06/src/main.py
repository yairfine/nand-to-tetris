import re
import sys
from pathlib import Path

C_INSTRUCTION_PTRN = "(?P<dest>[AMD]{1,3}=)?(?P<comp>[01\-AMD!|+&><]{1,3})(?P<jump>;[JGTEQELNMP]{3})?"

JUMP_REG_GROUP = "jump"
COMP_REG_GROUP = "comp"
DEST_REG_GROUP = "dest"

VARIABLE_START_ADDR = 16
LABEL_PREFIX_AND_SUFFIX = "()"
LABEL_SUFFIX = ")"
LABEL_PREFIX = "("
A_INSTRUCTION = "@"
ASM_EXT = "*.asm"
HACK_EXT = ".hack"
A_INSTRUCTION_FMT = "016b"


class Parser:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.clean_data = []
        self.symbols_table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3,
                              "THAT": 4, "R0": 0, "R1": 1, "R2": 2, "R3": 3,
                              "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8,
                              "R9": 9, "R10": 10, "R11": 11, "R12": 12,
                              "R13": 13, "R14": 14, "R15": 15, "SCREEN": 16384,
                              "KBD": 24576}

        self.dest_table = {None: "000", "M": "001", "D": "010", "MD": "011",
                           "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

        self.comp_table = {"0": "110101010", "1": "110111111",
                           "-1": "110111010", "D": "110001100",
                           "A": "110110000", "!D": "110001101",
                           "!A": "110110001", "-D": "110001111",
                           "-A": "110110011", "D+1": "110011111",
                           "1+D": "110011111", "A+1": "110110111",
                           "1+A": "110110111", "D-1": "110001110",
                           "A-1": "110110010", "D+A": "110000010",
                           "A+D": "110000010", "D-A": "110010011",
                           "A-D": "110000111", "D&A": "110000000",
                           "D|A": "110010101",
                           "M": "111110000", "!M": "111110001",
                           "-M": "111110011", "M+1": "111110111",
                           "1+M": "111110111", "M-1": "111110010",
                           "D+M": "111000010", "M+D": "111000010",
                           "D-M": "111010011", "M-D": "111000111",
                           "D&M": "111000000", "D|M": "111010101",
                           "D<<": "010110000", "D>>": "010010000",
                           "A<<": "010100000", "A>>": "010000000",
                           "M<<": "011100000", "M>>": "011000000"
                           }

        self.jump_table = {None: "000", "JGT": "001", "JEQ": "010",
                           "JGE": "011", "JLT": "100", "JNE": "101",
                           "JLE": "110", "JMP": "111"}

    def preprocessor(self):
        for line in self.raw_data:
            line = line.rstrip("\n\r")

            if re.search("^\s*$", line) or line.startswith('//'):
                continue

            elif line.startswith(LABEL_PREFIX) and line.endswith(LABEL_SUFFIX):
                label = line.strip(LABEL_PREFIX_AND_SUFFIX)
                self.symbols_table[label] = len(self.clean_data)

            else:
                no_comments_line = re.sub('(//).+', "", line)
                clean_line = re.sub('[ \t]+', "", no_comments_line)
                self.clean_data.append(clean_line)

    def load_variables(self):
        index = VARIABLE_START_ADDR
        for line in self.clean_data:
            if line.startswith(A_INSTRUCTION) and not (line[1:]).isdigit():
                variable = line.lstrip(A_INSTRUCTION)
                if variable not in self.symbols_table:
                    self.symbols_table[variable] = index
                    index += 1

    def parse_a_instruction(self, line):
        if line[1:] in self.symbols_table:
            number = self.symbols_table[line[1:]]
        else:
            number = int(line[1:])

        binary_number = format(number, A_INSTRUCTION_FMT)
        return binary_number

    def parse_c_instruction(self, line):
        result = re.match(C_INSTRUCTION_PTRN, line)

        dest = result.group(DEST_REG_GROUP)
        comp = result.group(COMP_REG_GROUP)
        jump = result.group(JUMP_REG_GROUP)

        if dest is not None:
            dest = dest.rstrip("=")
        if jump is not None:
            jump = jump.lstrip(";")

        binary_instruction = "1{}{}{}".format(self.comp_table[comp],
                                              self.dest_table[dest],
                                              self.jump_table[jump])

        return binary_instruction

    def parse(self):
        self.preprocessor()
        self.load_variables()

        binary_opcodes = []
        for line in self.clean_data:
            if line.startswith(A_INSTRUCTION):
                opcode = self.parse_a_instruction(line)
            else:
                opcode = self.parse_c_instruction(line)

            binary_opcodes.append(opcode)

        binary_data = "\n".join(binary_opcodes)
        binary_data += "\n"
        return binary_data


class Assembler:
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
            for file in input_path.glob(ASM_EXT):
                files.append(file)

        else:
            files.append(input_path)

        return files

    def run(self):
        files = self._glob()
        for file in files:
            with file.open("r") as fh:
                lines = fh.readlines()
            parser = Parser(lines)

            binary_code = parser.parse()
            output_filename = file.with_suffix(HACK_EXT)
            self._write_file(output_filename, binary_code)


if __name__ == '__main__':
    asm = Assembler()
    asm.run()
