import sys
from pathlib import Path

from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer

XML_EXT = ".xml"
JACK_EXT = "*.jack"

class SyntaxAnalyzer:
    def __init__(self):
        self._input_path = sys.argv[1]

    def _write_file(self, filename, xml_tree):
        xml_tree = xml_tree.replace('<?xml version="1.0" ?>\n', r"")
        filename.write_text(xml_tree)

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
            compilation_engine = CompilationEngine(tokenizer)
            xml_tree = compilation_engine.compileClass()

            self._write_file(file.with_suffix(XML_EXT), xml_tree)
