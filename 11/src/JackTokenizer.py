import re
from enum import Enum

KEYWORD_REGEX = "(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)(?:[ ;(){},])"
sss = "{|}|(|)|[|]|.|,|;|+|-|*|/|&|<|\||<|>|=|~"
SYMBOL_REGEX = "[{}()[\].,;+\-*/&<>|=~]"
IDENTIFIER_REGEX = "[a-zA-Z_]+[a-zA-Z0-9_]*"
INTEGER_CONST_REGEX = "[0-9]+"
STRING_CONST_REGEX = '"[^"\r\n]*"'

ALL_PATTERNS = [KEYWORD_REGEX, SYMBOL_REGEX, IDENTIFIER_REGEX, INTEGER_CONST_REGEX, STRING_CONST_REGEX]

class TokenType(Enum):
    keyword = 1
    symbol = 2
    identifier = 3
    integerConstant = 4
    stringConstant = 5


TYPE_BY_PATTERN = {KEYWORD_REGEX: TokenType.keyword,
                   SYMBOL_REGEX: TokenType.symbol,
                   IDENTIFIER_REGEX: TokenType.identifier,
                   INTEGER_CONST_REGEX: TokenType.integerConstant,
                   STRING_CONST_REGEX: TokenType.stringConstant}


class JackTokenizer:
    def __init__(self, stream):
        self.stream = stream
        self.preprocess()

        self.value_func_by_type = {
            TokenType.keyword: self.keyword,
            TokenType.symbol: self.symbol,
            TokenType.identifier: self.identifier,
            TokenType.integerConstant: self.intVal,
            TokenType.stringConstant: self.stringVal
        }

    def preprocess(self):
        self.stream = re.sub('^[ \t\f\v\n\r]+', "", self.stream, flags=re.MULTILINE)
        self.stream = re.sub('[ \t\f\v\n\r]+$', "", self.stream, flags=re.MULTILINE)
        self.stream = re.sub('\t+', " ", self.stream)
        self.stream = re.sub("^//.*", "", self.stream, flags=re.MULTILINE)


        self.stream = re.sub('(#[^"\n\r]*(?:"[^"\n\r]*"[^"\n\r]*)*[\r\n]|/\*([^*]|\*(?!/))*?\*/)(?=[^"]*(?:"[^"]*"[^"]*)*$)', "", self.stream)
        lines = self.stream.splitlines()
        self.stream = self.clean_comments(lines)

    def clean_comments(self, lines):
        result = []
        for line in lines:
            is_string = False
            line_length = len(line)
            prev_char = None
            for pos, char in enumerate(line):
                if char == '"':
                    is_string = not(is_string)
                if prev_char == "/" and char == "/" and is_string is False:
                    line_length = pos - 1
                    break
                prev_char = char
            result.append(line[:line_length])
        return " ".join(result)

    def hasMoreToken(self):
        for pattern in ALL_PATTERNS:
            if re.match(pattern, self.stream):
                return True
        return False

    def advance(self):
        length = len(self.get_raw_value())
        self.stream = self.stream[length:]
        self.stream = self.stream.lstrip(" ")

    def tokenType(self):
        self.stream = self.stream.lstrip(" ")
        for pattern, type in TYPE_BY_PATTERN.items():
            if re.match(pattern, self.stream):
                return type

    def keyword(self):
        token = re.match(KEYWORD_REGEX, self.stream)
        return token.groups()[0]

    def symbol(self):
        token = re.match(SYMBOL_REGEX, self.stream)
        return token.group()

    def identifier(self):
        token = re.match(IDENTIFIER_REGEX, self.stream)
        return token.group()

    def intVal(self):
        token = re.match(INTEGER_CONST_REGEX, self.stream)
        return token.group()

    def stringVal(self):
        token = re.match(STRING_CONST_REGEX, self.stream)
        token = token.group()
        return token

    def get_value(self):
        return self.get_raw_value()

    def get_raw_value(self):
        token_type = self.tokenType()
        value_func = self.value_func_by_type[token_type]
        return value_func()

    def previewNext(self):
        if self.stream == "":
            return ""
        preview = JackTokenizer(self.stream)
        preview.advance()
        if preview.hasMoreToken() is False:
            return ""
        return preview.get_value()
