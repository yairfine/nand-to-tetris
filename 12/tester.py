import os
from pathlib import Path
from shutil import copyfile

JACK_EXT = "*.jack"
VM_EXT = "*.vm"

MAIN_PATH = r"C:\nand2tetrisEnv\projects\12";

PATHS = [
    r"C:\nand2tetrisEnv\projects\12\MemoryTestTst",
    r"C:\nand2tetrisEnv\projects\12\OutputTest",
    r"C:\nand2tetrisEnv\projects\12\ScreenTest",
    r"C:\nand2tetrisEnv\projects\12\StringTest",
    r"C:\nand2tetrisEnv\projects\12\SysTest",
    r"C:\nand2tetrisEnv\projects\12\ArrayTestTst",
    r"C:\nand2tetrisEnv\projects\12\KeyboardTest",
    r"C:\nand2tetrisEnv\projects\12\MathTestTst",
    r"C:\nand2tetrisEnv\projects\12\Games\Average",
    r"C:\nand2tetrisEnv\projects\12\Games\ComplexArrays",
    r"C:\nand2tetrisEnv\projects\12\Games\ConvertToBin",
    r"C:\nand2tetrisEnv\projects\12\Games\fallingBall",
    r"C:\nand2tetrisEnv\projects\12\Games\FlappyBird",
    r"C:\nand2tetrisEnv\projects\12\Games\NinaGame",
    r"C:\nand2tetrisEnv\projects\12\Games\Pong",
    r"C:\nand2tetrisEnv\projects\12\Games\RoniGame",
    r"C:\nand2tetrisEnv\projects\12\Games\Seven",
    r"C:\nand2tetrisEnv\projects\12\Games\Square",
    r"C:\nand2tetrisEnv\projects\12\Games\YehonatanGame",

    r"C:\nand2tetrisEnv\projects\12\drive_test\ArrayTest",
    r"C:\nand2tetrisEnv\projects\12\drive_test\KeyboardTest",   
    r"C:\nand2tetrisEnv\projects\12\drive_test\MathTest",
    r"C:\nand2tetrisEnv\projects\12\drive_test\MemoryTest",   
    r"C:\nand2tetrisEnv\projects\12\drive_test\MemoryTest2",
    r"C:\nand2tetrisEnv\projects\12\drive_test\MemoryTest3",   
    r"C:\nand2tetrisEnv\projects\12\drive_test\OutputTest",
    r"C:\nand2tetrisEnv\projects\12\drive_test\ScreenTest",
    r"C:\nand2tetrisEnv\projects\12\drive_test\String2Test",
    r"C:\nand2tetrisEnv\projects\12\drive_test\StringTest",   
    r"C:\nand2tetrisEnv\projects\12\drive_test\SysTest",
]

def glob(path, extension):
    files = []
    input_path = path

    if input_path.is_dir():
        for jack_file in input_path.glob(extension):
            files.append(jack_file)

    else:
        files.append(input_path)

    return files


def to_pathlibs(pathes, EXT):
    pathlibs = []

    for path in PATHS:
        pathlib = Path(path.format(EXT))
        pathlibs.append(pathlib)

    return pathlibs



def compile():
    for test_dir in PATHS:
        test_dir = Path(test_dir)
        main_dir = Path(MAIN_PATH)
        for jack_file in main_dir.glob(JACK_EXT):
            copyfile(jack_file, test_dir / jack_file.name)

        print(f"Compiling the files in {test_dir.name} using the official compiler:")
        os.system(fr'C:\nand2tetrisEnv\tools\JackCompiler.bat {test_dir}')

        print(f"Finished handling {test_dir.name}.\n\n")


if __name__ == "__main__":
    compile()
