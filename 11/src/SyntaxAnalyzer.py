from pathlib import Path

from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter

VM_EXT = ".vm"
XML_EXT = ".xml"
JACK_EXT = "*.jack"


class SyntaxAnalyzer:
    def __init__(self, path):
        self._input_path = path

    def _glob(self):
        files = []
        input_path = Path(self._input_path)

        if input_path.is_dir():
            for file in input_path.glob(JACK_EXT):
                files.append(file)

        else:
            files.append(input_path)

        return files

    def run(self):
        files = self._glob()

        for file in files:
            with file.open("r") as f:
                data = f.read()
            tokenizer = JackTokenizer(data)
            vm_writer = VMWriter(file.with_suffix(VM_EXT))
            engine = CompilationEngine(tokenizer, vm_writer)
            engine.compile_class()
            vm_writer.close()
