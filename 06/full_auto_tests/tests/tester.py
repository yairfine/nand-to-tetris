import os
from typing import List, Tuple

# INSTRUCTIONS:
# 1. Unzip tester.py along with `tests` folder
# 2. Update ASSEMBLER_CMD so the tester can run your assembler through the command line
# 3. On windows run `python tester.py`, otherwise `python3 tester.py`

# Command line to run your assembler (without a parameter)
# ASSEMBLER_CMD = "./Assembler"
ASSEMBLER_CMD = "python ./src/main.py"
# ASSEMBLER_CMD = "python3 Main.py"

# Path to directory of test files (.asm & .cmp for each test)
TEST_DIR = "tests"


def cmp_files(expected, out):
    for line, (expected_line, out_line) in enumerate(zip(expected, out), 1):
        if expected_line != out_line:
            print("FAILED comparison in line", line)
            print("\t\tExpected `", expected_line, "`, ",
                  "got `", out_line, "`",
                  sep="")
            print()
            return False

    print("Passed comparison")
    return True


def load_tests(dir_path) -> List[Tuple[str, str]]:
    tests = list()

    for file in os.listdir(dir_path):
        file_name, file_ext = os.path.splitext(file)

        if file_ext == ".asm":
            test_path = os.path.join(dir_path, file_name)
            tests.append((file_name, test_path))

    return tests


if __name__ == '__main__':
    print("~ Tester for Project 6 (Assembler) in Nand to Tetris, 2020/21 Fall ~")
    print("~ Based on tests from the drive and from the project page ~")

    print()
    print("Note: The tester expects a trailing new line,",
          "but ignores the type of the new line characters.")

    print()
    print("Collecting test files...")

    print()

    dir_path = TEST_DIR
    tests = load_tests(dir_path)

    choice_should_delete = input(
        "Remove the old output files, if such exist? (Type y/n and press Enter) "
    )

    if choice_should_delete == 'y':
        print("Deleting old output files...")

        for test, test_path in tests:
            out_file_path = test_path + ".hack"
            if os.path.isfile(out_file_path):
                os.remove(out_file_path)

    print()
    print("Running your assembler on the test directory...")

    ret_code = os.system(ASSEMBLER_CMD + " " + TEST_DIR)

    if ret_code != 0:
        print("ASSEMBLER FAILED with return code: ", ret_code)
        print("\tNote: Make sure you have set ASSEMBLER_CMD correctly.")
        print("\tASSEMBLER_CMD:", ASSEMBLER_CMD)

    print()
    print("Comparing output...")

    fails = list()

    for test, test_path in tests:
        cmp_path = test_path + ".cmp"
        out_path = test_path + ".hack"

        print("\tChecking", test, end=": ")

        passed = False
        if not os.path.exists(out_path):
            print("FAILED, output file doesn't exist")
        else:
            cmp_file = open(cmp_path, "r")
            out_file = open(out_path, "r")
            passed = cmp_files(cmp_file, out_file)

        if not passed:
            fails.append(test)

    print()

    if fails:
        print("SUMMARY - FAILED", len(fails), "OUT OF", len(tests), "FILES:")
        print(fails)

    else:
        print("All tests passed successfully :)")
