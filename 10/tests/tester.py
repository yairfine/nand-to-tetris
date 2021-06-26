import os
import sys
import subprocess

# INSTRUCTIONS:
# 1. Unzip tester.py along with `tests` folder
# 2. Update JACK_ANALYZER_CMD so the tester can run your analyzer through the command line
# 3. On windows run `python -u tester.py`, otherwise `python3 -u tester.py`
#    [INSIDE THE SAME FOLDER USING `cd`]
#
# You might need to set execute permissions for TextComparer.sh first:
#     chmod u+rwx ../../tools/TextComparer.sh

# TEXT_COMPARER = r"../../tools/TextComparer.sh"
TEXT_COMPARER = r"C:\nand2tetrisEnv\tools\TextComparer.bat"

# Command line to run your analyzer (without a parameter)
# JACK_ANALYZER_CMD = r"./JackAnalyzer"  # if JackAnalyzer - files must be in same directory
JACK_ANALYZER_CMD = r"python ..\src\main.py"
# JACK_ANALYZER_CMD = "python3 src/Main.py"

# Path to directory of test files (.xml & .xml.cmp for each test)
TEST_DIR = "tests"
IN_SUFFIX = ".jack"
OUT_SUFFIX = ".xml"
CMP_SUFFIX = ".xml.cmp"


def run_cmd(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as p:
        sys.stdout.flush()
        out = p.stdout.read()
        sys.stdout.buffer.write(out)
        print()
        sys.stdout.flush()


def cmp_files(expected, out):
    print(TEXT_COMPARER + ' ' + expected + ' ' + out)
    run_cmd(TEXT_COMPARER + ' ' + expected + ' ' + out)


if __name__ == '__main__':
    print("~ Tester for Project 10 (JackAnalyzer)'"
          " in Nand to Tetris, 2020/21 Fall ~")
    print()

    print("Runs tests from the drive, either file-by-file or directory-by-directory.")
    print()

    print("IMPORTANT NOTE!")
    print("MAKE SURE YOU HAVE CORRECTLY SET THE CONSTANTS IN THE HEAD OF THE TESTER FILE.")
    print("In any case, please back up your files (in case your program has output-related bugs).")
    print()
    print("TEXT_COMPARER:", TEXT_COMPARER)
    print("JACK_ANALYZER_CMD:", JACK_ANALYZER_CMD)
    print()

    should_run_on_files = input(
        "Enter 'f' to run your JackAnalyzer file-by-file. " +
        "Othwerwise it'll run directory-by-directory."
    ) == "f"

    print()
    print("Collecting test files...")

    print()

    dir_path = TEST_DIR

    tests = list()
    old_out_files = list()
    test_folders = set()

    for root, dirs, files in os.walk(TEST_DIR):
        for name in files:
            file_path = os.path.join(root, name)

            if name.endswith(CMP_SUFFIX):
                tests.append(file_path[:-len(CMP_SUFFIX)])
                dir_path = os.path.dirname(file_path)
                test_folders.add(dir_path)

            elif name.endswith(OUT_SUFFIX):
                old_out_files.append(file_path)

    if not test_folders:
        print("Didn't find the tests folder...")
        print("Please rerun as instructed from the command line in the same folder.")
        exit()

    test_folders = sorted(test_folders)

    if old_out_files:
        should_clean_files = input(
            "Found some old .xml files in the tests folder. " +
            "Delete them first? (Enter y/n)"
        ) == "y"

        if should_clean_files:
            for path in old_out_files:
                if os.path.isfile(path):
                    os.remove(path)

    print()

    if should_run_on_files:
        in_paths = (file_path + IN_SUFFIX for file_path in tests)
        print("Running your JackAnalyzer on the test files...")
    else:
        in_paths = test_folders
        print("Running your JackAnalyzer on the test directories...")

    for in_path in in_paths:
        print('\tPath:', in_path)
        ret_code = os.system(JACK_ANALYZER_CMD + " " + in_path)

        if ret_code != 0:
            print("JackAnalyzer FAILED with return code: ", ret_code)
            print("\tNote: Make sure you have set JACK_ANALYZER_CMD correctly.")
            print("\tJACK_ANALYZER_CMD:", JACK_ANALYZER_CMD)
            print()

    print()
    print("Comparing output...")

    for test in tests:
        cmp_path = test + '.xml.cmp'
        out_path = test + '.xml'

        print()
        print("Checking: ", test)
        cmp_files(cmp_path, out_path)

    print()
    print()
    print("CHECK THE RESULTS OF THE TEXT COMPARER ABOVE.")
    print("Each of them is supposed to be: "
          '"Comparison ended successfully"')
