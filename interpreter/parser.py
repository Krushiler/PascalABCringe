from .token import Token, TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOp, Var, Assign, ComplexStatement, EmptyNode, Block


class Parser:
    def __init__(self):
        self._current_token = None
        self._lexer = Lexer()

    def check_token(self, type_: TokenType):
        while self._current_token and self._current_token.type_ == TokenType.EOL:
            self._current_token = self._lexer.next()
        if self._current_token and self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            raise SyntaxError("Invalid token order")

    def block(self):
        declarations = self.declarations()
        complex_statement = self.complex_statement()
        node = Block(declarations, complex_statement)
        return node

    def declarations(self):
        declarations = []
        while self._current_token and self._current_token.type_ == TokenType.ID:
            declarations.append(self.variable_declaration())
            self.check_token(TokenType.SEMICOLON)
        return declarations

    def variable_declaration(self):
        nodes = [Var(self._current_token)]
        self.check_token(TokenType.ID)
        while self._current_token and self._current_token.type_ == TokenType.COMMA:
            self.check_token(TokenType.COMMA)
            nodes.append(Var(self._current_token))
            self.check_token(TokenType.ID)
        self.check_token(TokenType.SEMICOLON)

        return nodes

    def complex_statement(self):
        self.check_token(TokenType.BEGIN)
        nodes = self.statement_list()
        self.check_token(TokenType.END)
        root = ComplexStatement()

        for statement in nodes:
            root.children.append(statement)

        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self._current_token and self._current_token.type_ == TokenType.SEMICOLON:
            self.check_token(TokenType.SEMICOLON)
            results.append(self.statement())

        if self._current_token and self._current_token.type_ == TokenType.ID:
            raise SyntaxError("Invalid statement")
        return results

    def statement(self):
        if self._current_token and self._current_token.type_ == TokenType.BEGIN:
            node = self.complex_statement()
        elif self._current_token and self._current_token.type_ == TokenType.ID:
            node = self.assign()
        else:
            node = self.empty()
        return node

    def assign(self):
        left = self.variable()
        token = self._current_token
        self.check_token(TokenType.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        token = self._current_token
        self.check_token(TokenType.ID)
        return Var(token)

    def factor(self):
        token = self._current_token
        if not token:
            raise SyntaxError("Invalid factor")
        elif token.type_ == TokenType.NUMBER:
            self.check_token(TokenType.NUMBER)
            return Number(token)
        elif token.type_ == TokenType.ID:
            self.check_token(TokenType.ID)
            return Var(token)
        elif token.type_ == TokenType.LPAREN:
            self.check_token(TokenType.LPAREN)
            result = self.expr()
            self.check_token(TokenType.RPAREN)
            return result
        elif token.type_ == TokenType.OPERATOR and token.value in ["+", "-"]:
            self.check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.factor())
        raise SyntaxError("Invalid factor")

    def term(self):
        result = self.factor()
        while (self._current_token
               and self._current_token.type_ == TokenType.OPERATOR
               and self._current_token.value in ["*", "/"]):
            token = self._current_token
            self.check_token(TokenType.OPERATOR)
            return BinOp(result, token, self.factor())
        return result

    def expr(self):
        result = self.term()
        while self._current_token and self._current_token.type_ == TokenType.OPERATOR:
            token = self._current_token
            self.check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.term())
        return result

    def empty(self):
        return EmptyNode()

    def parse(self, code):
        self._lexer.init(code)
        self._current_token = self._lexer.next()
        result = self.block()
        self.check_token(TokenType.DOT)
        return result
