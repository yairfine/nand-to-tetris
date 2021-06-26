import os

# INSTRUCTIONS
# 1. Unzip the files (tester.py and tests must be in the same directory as VMtranslator)
# 2. Review/update the two constants if necessary
#    Not necessary if running on Unix and you added VMtranslator as instructed (and run make before)
# 3. Run `python3 tester.py` on Unix or `python tester.py` on Windows
#    [IN THE SAME DIRECTORY using `cd`]
#
# You might need to set execute permissions for CPUEmulator.sh first:
#     chmod u+rwx ../../tools/CPUEmulator.sh

# Same as project 7 (only without path tests)
# Along with the matching project 8 tests from the drive


# Path to the CPU Emulator (.bat if on Windows, .sh if on Unix)
CPU_EMULATOR_PATH = r"C:\nand2tetrisEnv\tools\CPUEmulator.bat"
# CPU_EMULATOR_PATH = r"..\..\tools\CPUEmulator.bat"

# Command to run your VM Translator
# VM_TRANSLATOR_COMMAND = "./VMtranslator"  # if VMTranslator - files must be in same directory
VM_TRANSLATOR_COMMAND = "python main.py"
# VM_TRANSLATOR_COMMAND = r"python3 src/Main.py"
# VM_TRANSLATOR_COMMAND = "java Main"


def run_vm_translator(in_path):
    os.system(VM_TRANSLATOR_COMMAND + " " + in_path)


def clean_files(file_paths):
    should_clean_files = False

    if file_paths:
        should_clean_files = input(
            "Found some old .ASM files in the tests folder. " +
            "Delete them first? (Enter y/n)"
        ) == "y"
        print()

    if should_clean_files:
        for file_path in file_paths:
            os.remove(file_path)


def remove_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def main():
    test_folders = set()
    test_files = list()
    asm_files = list()
    vm_files = list()

    print("~ Auto Tester for Project 8 in Nand to Tetris (Fall 2020/21) ~")
    print()

    print("Contains tests from the moodle and from the drive.")
    print()

    print("IMPORTANT NOTE!")
    print("MAKE SURE YOU HAVE CORRECTLY SET THE CONSTANTS IN THE HEAD OF THE TESTER FILE.")
    print("In any case, please back up your files (in case your program has output-related bugs).")
    print()
    print("CPU_EMULATOR_PATH:", CPU_EMULATOR_PATH)
    print("VM_TRANSLATOR_PATH:", VM_TRANSLATOR_COMMAND)
    print()
    _ = input("Press ENTER to continue.")
    print()

    print("Collecting test files... (Feel free to add more directories under `tests`)")
    print()

    for root, dirs, files in os.walk("tests"):
        for name in files:
            file_path = os.path.join(root, name)

            if file_path.endswith(".asm"):
                asm_files.append(file_path)

            elif file_path.endswith(".vm"):
                vm_files.append(file_path)

            elif file_path.endswith(".tst") and not file_path.endswith("VME.tst"):
                test_files.append(file_path)
                dir_path = os.path.dirname(file_path)
                test_folders.add(dir_path)

    if not test_files:
        print("Didn't find the tests folder...")
        print("Please rerun as instructed from the command line in the same folder")
        return
    
    clean_files(asm_files)

    print("Running your VM Translator on the test directories one-by-one...")
    for test_folder in sorted(test_folders):
        print("\tDirectory:", test_folder)
        run_vm_translator(test_folder)

    print()
    print("Running the tests using the CPUEmulator...")
    print()

    for test_file in test_files:
        print("Test file:", test_file)
        os.system(CPU_EMULATOR_PATH + " " + test_file)
        print()

    print()
    print("CHECK THE RESULTS OF THE CPU EMULATOR COMPARISONS.")
    print()
    print("Most of them should be: "
          '"End of script - Comparison ended successfully".')
    print('Except Pong - "End of script", but maybe "Program too large" is enough.')
    print()
    print("If you've succedded in Reversi, Reversi2 or Snake - contact Shimon Shocken!")
    print('Otherwise you probably got "Program too large" like the rest of us :)')
    print()


if __name__ == "__main__":
    main()
