import sys

from SyntaxAnalyzer import SyntaxAnalyzer

if __name__ == "__main__":
    analyzer = SyntaxAnalyzer(sys.argv[1])
    analyzer.run()