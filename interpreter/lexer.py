from .token import Token, TokenType

keywords = {
    "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
    "END": Token(TokenType.END, "END"),
}


class Lexer:
    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def init(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]

    def forward(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def skip(self):
        while (self._current_char is not None and
               self._current_char.isspace()):
            self.forward()

    def number(self):
        result = []
        while (self._current_char and
               (self._current_char.isdigit() or
                self._current_char == ".")):
            result.append(self._current_char)
            self.forward()
        return "".join(result)

    def colon(self):
        self.forward()
        while self._current_char and self._current_char.isspace():
            self.forward()
        if self._current_char and self._current_char == "=":
            self.forward()
            return Token(TokenType.ASSIGN, ":=")
        return Token(TokenType.COLON, ":")

    def keyword(self):
        result = ''
        while (self._current_char is not None and
               self._current_char.isalnum()):
            result += self._current_char
            self.forward()
        return keywords.get(result, Token(TokenType.ID, result))

    def next(self):
        while self._current_char:
            if self._current_char.isspace():
                self.skip()
                continue
            if self._current_char.isalpha():
                return self.keyword()
            if self._current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())
            if self._current_char in ["+", "-", "/", "*"]:
                op = self._current_char
                self.forward()
                return Token(TokenType.OPERATOR, op)
            if self._current_char == "(":
                op = self._current_char
                self.forward()
                return Token(TokenType.LPAREN, op)
            if self._current_char == ")":
                op = self._current_char
                self.forward()
                return Token(TokenType.RPAREN, op)
            if self._current_char == ".":
                op = self._current_char
                self.forward()
                return Token(TokenType.DOT, op)
            if self._current_char == ":":
                return self.colon()
            if self._current_char == ";":
                op = self._current_char
                self.forward()
                return Token(TokenType.SEMICOLON, op)
            if self._current_char == ".":
                op = self._current_char
                self.forward()
                return Token(TokenType.DOT, op)
            if self._current_char == "=":
                op = self._current_char
                self.forward()
                return Token(TokenType.ASSIGN, op)
            if self._current_char == ",":
                op = self._current_char
                self.forward()
                return Token(TokenType.COMMA, op)
            if self._current_char == "\n":
                op = self._current_char
                self.forward()
                return Token(TokenType.EOL, op)

            raise SyntaxError("Bad token")
