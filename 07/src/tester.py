import os

# INSTRUCTIONS
# 1. Unzip the files (tester.py and tests must be in the same directory as VMtranslator)
# 2. Review/update the two constants if necessary
#    Not necessary if running on Unix and you added VMtranslator as instructed (and run make before)
# 3. Run `python3 tester.py` on Unix or `python tester.py` on Windows

# Path to the CPU Emulator (.bat if on Windows, .sh if on Unix)
CPU_EMULATOR_PATH = r'"C:\Users\Yuser\Dropbox\Studies\Year_2\Semester_A\NAND_to_Tetris\tools\CPUEmulator.bat"'
# CPU_EMULATOR_PATH = r"..\..\tools\CPUEmulator.bat"

# Command to run your VM Translator
# VM_TRANSLATOR_COMMAND = "V/Mtranslator"  # if VMTranslator - files must be in same directory
VM_TRANSLATOR_COMMAND = "python main.py"
# VM_TRANSLATOR_COMMAND = "python Main.py"
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


def automatic_tests():
    print()
    should_run = input(
        "Run basic automatic output file naming and location tests?\n" +
        "This includes automatically creating/deleting test files.\n" +
        "(Enter y/n)"
    ) == "y"
    print()

    if not should_run:
        print("May the odds be ever in your favor :)")
        return

    test_dir = "tests"
    auto_dir = os.path.join(test_dir, "Auto")
    multi_folder = os.path.join(auto_dir, "MultiFileFolder")
    multi_folder_asm = os.path.join(multi_folder, "MultiFileFolder.asm")
    file_a = os.path.join(multi_folder, "FileA")
    file_b = os.path.join(multi_folder, "FileB")

    if not os.path.isdir(auto_dir):
        print("Too bad the supplied Auto test folder isn't here...")
        return

    print("Cleaning up...")

    for root, dirs, files in os.walk(auto_dir):
        for name in files:
            file_path = os.path.join(root, name)
            if file_path.endswith(".asm"):
                os.remove(file_path)

    print()

    print("Running tests... If there's any assertion error you'll see it.")
    print()

    print("RUNNING TEST 1. Relative path to folder with multiple files...")
    run_vm_translator(multi_folder)
    assert os.path.isfile(multi_folder_asm)
    assert not os.path.exists(file_a + ".asm")
    assert not os.path.exists(file_b + ".asm")
    os.remove(multi_folder_asm)

    print("RUNNING TEST 2. Relative path to file in a multi-file folder...")
    run_vm_translator(file_a + ".vm")
    assert os.path.isfile(file_a + ".asm")
    assert not os.path.exists(multi_folder_asm)
    assert not os.path.exists(file_b + ".asm")
    os.remove(file_a + ".asm")

    print("RUNNING TEST 3. Absolute path to folder...")
    run_vm_translator(os.path.abspath(multi_folder))
    assert os.path.isfile(multi_folder_asm)
    assert not os.path.exists(file_a + ".asm")
    assert not os.path.exists(file_b + ".asm")
    os.remove(multi_folder_asm)

    run_vm_translator(os.path.join(os.path.abspath(multi_folder), ""))
    assert os.path.isfile(multi_folder_asm)
    os.remove(multi_folder_asm)

    print("RUNNING TEST 4. Absolute path to file...")
    run_vm_translator(os.path.abspath(file_b) + ".vm")
    assert os.path.isfile(file_b + ".asm")
    assert not os.path.exists(multi_folder_asm)
    assert not os.path.exists(file_a + ".asm")
    os.remove(file_b + ".asm")
    print("Great.")

    print()
    print("More things to test yourself "
          "(didn't want to accidentally mess with your files/folders):")
    print()
    print("\t- Relative path to current folder (output should be named after the folder)")
    print("\t- Relative path to a file in the current folder "
          "(output should be named after the file)")
    print("\t- Relative path to a file/directory in parent folder")

    print()
    print("That's it :)")


def main():
    test_folders = set()
    test_files = list()
    asm_files = list()
    vm_files = list()

    print("~ Auto Tester for Project 7 in Nand to Tetris (Fall 2020/21) ~")
    print()

    print("Contains tests from the moodle, from the drive,")
    print("and some automatic output file naming and location tests.")
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
    print("Each of them is supposed to be: "
          '"End of script - Comparison ended successfully"')
    print()

    automatic_tests()


if __name__ == "__main__":
    main()
