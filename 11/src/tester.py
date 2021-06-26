from pathlib import Path

from SyntaxAnalyzer import SyntaxAnalyzer
import os
from shutil import copyfile

JACK_EXT = "*.jack"
VM_EXT = "*.vm"

PATHS = [
    r"C:\nand2tetrisEnv\projects\11\Seven",
    r"C:\nand2tetrisEnv\projects\11\ConvertToBin",
    r"C:\nand2tetrisEnv\projects\11\Square",
    r"C:\nand2tetrisEnv\projects\11\Average",
    r"C:\nand2tetrisEnv\projects\11\Pong",
    r"C:\nand2tetrisEnv\projects\11\ComplexArrays",
    r"C:\nand2tetrisEnv\projects\11\NinaGame",
    r"C:\nand2tetrisEnv\projects\11\YehonatanGame",
    r"C:\nand2tetrisEnv\projects\11\FlappyBird",
    r"C:\nand2tetrisEnv\projects\11\RoniGame",
    r"C:\nand2tetrisEnv\projects\11\fallingBall"
]


def glob(path, extension):
    files = []
    input_path = path

    if input_path.is_dir():
        for file in input_path.glob(extension):
            files.append(file)

    else:
        files.append(input_path)

    return files


def to_pathlibs(pathes):
    pathlibs = []

    for path in PATHS:
        pathlib = Path(path)
        pathlibs.append(pathlib)

    return pathlibs


def run():
    for path in to_pathlibs(PATHS):
        out_path = path / "output"
        cmp_path = path / "compare"
        try:
            os.mkdir(out_path)
            os.mkdir(cmp_path)
        except FileExistsError:
            pass

        for file in glob(path, JACK_EXT):
            copyfile(file, out_path / file.name)
            copyfile(file, cmp_path / file.name)

        print(f"Compiling the files in {path.name} using the official compiler:")
        os.system(fr'C:\nand2tetrisEnv\tools\JackCompiler.bat {cmp_path}')

        print(f"Compiling the files in {path.name} using our compiler.")
        s = SyntaxAnalyzer(out_path)
        s.run()
        print(f"Finished handling {path.name}.\n\n")


if __name__ == "__main__":
    run()
