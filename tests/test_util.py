import pytest

from interpreter import Interpreter
from interpreter.ast import Number, BinOp, UnaryOp
from interpreter.interpreter import NodeVisitor
from interpreter.parser import Parser
from interpreter.token import Token, TokenType


# @pytest.fixture(scope="function")
# def interpreter():
#     return Interpreter()
#
#
# @pytest.fixture(scope="function")
# def parser():
#     return Parser()
#
#
# class TestUtil:
#     def test_number_str(self):
#         assert str(Number(1)) == "Number (1)"
#
#     def test_binop_str(self):
#         assert str(BinOp(Number(1), Token(TokenType.OPERATOR, "+"), Number(2))) == "BinOp+ (Number (1), Number (2))"
#
#     def test_unop_str(self):
#         assert str(UnaryOp(Token(TokenType.OPERATOR, "-"), Number(1))) == "UnaryOp- (Number (1))"
#
#     def test_pass(self):
#         assert NodeVisitor().visit(BinOp(Number(1), Token(TokenType.OPERATOR, "S"), Number(2))) is None
#
#     def test_interpreter_visit_error(self, interpreter):
#         with pytest.raises(ValueError):
#             assert interpreter.visit("S")
#
#     def test_interpreter_visit_binop_error(self, interpreter):
#         with pytest.raises(ValueError):
#             assert interpreter.visit(BinOp(Number(1), Token(TokenType.OPERATOR, "S"), Number(2)))
#
#     def test_interpreter_visit_unaryop_error(self, interpreter):
#         with pytest.raises(ValueError):
#             assert interpreter.visit(UnaryOp(Token(TokenType.OPERATOR, "S"), Number(1)))
#
#     def test_incorrect_token_order(self, parser):
#         with pytest.raises(SyntaxError):
#             parser.check_token(TokenType.NUMBER)
#
#     def test_invalid_factor(self, parser):
#         with pytest.raises(SyntaxError):
#             parser.factor()
#
#     def test_interpreter_invalid_factor(self, interpreter):
#         with pytest.raises(SyntaxError):
#             interpreter.eval("5+()")
#
#     def test_token_str(self, parser):
#         assert str(Token(TokenType.NUMBER, "1")) == "Token(TokenType.NUMBER, 1)"
