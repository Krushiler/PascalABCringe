import pytest

from interpreter import Interpreter
from interpreter.ast import Node, Number, UnaryOp, BinOp
from interpreter.parser import Parser
from interpreter.token import TokenType, Token


@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()


def run_interpreter(interpreter: Interpreter, code: str) -> str:
    return interpreter.eval(f'BEGIN\n{code}\nEND.')


class TestInterpreter:

    def test_add(self, interpreter):
        assert run_interpreter(interpreter, "x:=2+2") == {'x': 4}

    def test_sub(self, interpreter):
        assert run_interpreter(interpreter, "x:=2-2") == {'x': 0}

    def test_mul(self, interpreter):
        assert run_interpreter(interpreter, "x:=2*2") == {'x': 4}

    def test_wrong_operator(self, interpreter):
        with pytest.raises(SyntaxError):
            run_interpreter(interpreter, "2&3")

    def test_add_spaces(self, interpreter):
        assert run_interpreter(interpreter, "x:=2 +      2") == {'x': 4}

    def test_div(self, interpreter):
        assert run_interpreter(interpreter, "x:=2/2") == {'x': 1}

    def test_unary_minus(self, interpreter):
        assert run_interpreter(interpreter, "x:=-2") == {'x': -2}

    def test_unary_plus(self, interpreter):
        assert run_interpreter(interpreter, "x:=+2") == {'x': 2}

    def test_unary_expression(self, interpreter):
        assert run_interpreter(interpreter, "x:=-2-2") == {'x': -4}

    def test_expression_priority(self, interpreter):
        assert run_interpreter(interpreter, "x:=2+2*2") == {'x': 6}

    def test_unary_expression_paren(self, interpreter):
        assert run_interpreter(interpreter, "x:=-(-(2+2))") == {'x': 4}

    def test_binary_unary_expression(self, interpreter):
        assert run_interpreter(interpreter, "x:=-(2 + 2 * 4)") == {'x': -10}

    def test_variables_expression(self, interpreter):
        assert run_interpreter(interpreter, "x:=-1; y:=x+1; z:=y*x") == {'x': -1, 'y': 0, 'z': 0}

    def test_nested_blocks(self, interpreter):
        assert run_interpreter(interpreter, "x:=5;\n BEGIN\n y:=x+1;\n END\n") == {'x': 5, 'y': 6}

    def test_unknown_token(self, interpreter):
        with pytest.raises(SyntaxError):
            run_interpreter(interpreter, "☺")

    def test_unknown_variable(self, interpreter):
        with pytest.raises(ValueError):
            run_interpreter(interpreter, "x: =y;")

    def test_invalid_statement(self, interpreter):
        with pytest.raises(ValueError):
            run_interpreter(interpreter, "x := x;")

    def test_invalid_token_order(self, interpreter):
        with pytest.raises(SyntaxError):
            run_interpreter(interpreter, "1; 2")

    def test_invalid_node(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit(Node)

    def test_invalid_unary_operator(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit_unaryop(UnaryOp(Token(TokenType.OPERATOR, "shit"), Number(Token(TokenType.NUMBER, "1"))))

    def test_invalid_binary_operator(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit_binop(BinOp(Number(Token(TokenType.NUMBER, "1")), Token(TokenType.OPERATOR, "fuck"),
                                          Number(Token(TokenType.NUMBER, "2"))))

    def test_empty_colon(self, interpreter):
        with pytest.raises(SyntaxError):
            run_interpreter(interpreter, ":")

    def test_empty_eol(self, interpreter):
        assert run_interpreter(interpreter, "\n") == {}

    def test_end_without_dot(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN\nEND")

    def test_invalid_factor(self, interpreter):
        with pytest.raises(SyntaxError):
            parser = Parser()
            parser._current_token = Token(TokenType.DOT, ".")
            parser.factor()

    def test_invalid_factor_is_null(self, interpreter):
        with pytest.raises(SyntaxError):
            Parser().factor()
