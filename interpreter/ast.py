from .token import Token


class Node:
    pass


class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):  # pragma: no cover
        return f"Number ({self.token})"


class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):  # pragma: no cover
        return f"BinOp{self.op.value} ({self.left}, {self.right})"


class UnaryOp(Node):
    def __init__(self, op: Token, number: Node):
        self.op = op
        self.number = number

    def __str__(self):  # pragma: no cover
        return f"UnaryOp{self.op.value} ({self.number})"


class Assign(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):  # pragma: no cover
        return f"Assign ({self.left}, {self.op}, {self.right})"


class Var(Node):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __str__(self):  # pragma: no cover
        return f"Var ({self.token})"


class ComplexStatement(Node):
    def __init__(self):
        self.children = []

    def __str__(self):  # pragma: no cover
        return f"ComplexStatement ({self.children})"


class Block(Node):
    def __init__(self, complex_statement: Node):
        self.complex_statement = complex_statement

    def __str__(self):  # pragma: no cover
        return f"Block ({self.complex_statement})"


class EmptyNode(Node):
    def __init__(self):
        pass

    def __str__(self):  # pragma: no cover
        return "EmptyNode"
