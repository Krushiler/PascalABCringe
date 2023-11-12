from .parser import Parser
from .ast import Number, BinOp, UnaryOp, Assign, Var, ComplexStatement, EmptyNode, Block


class NodeVisitor:

    def visit(self, node):
        pass


class Interpreter(NodeVisitor):

    def __init__(self):
        self.parser = Parser()
        self.scope = {}

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unaryop(node)
        elif isinstance(node, Assign):
            return self.visit_assign(node)
        elif isinstance(node, Var):
            return self.visit_var(node)
        elif isinstance(node, ComplexStatement):
            return self.visit_complex_statement(node)
        elif isinstance(node, EmptyNode):
            return None
        elif isinstance(node, Block):
            return self.visit_block(node)
        else:
            raise ValueError("Invalid node")

    def visit_assign(self, node):
        var_name = node.left.value
        self.scope[var_name] = self.visit(node.right)

    def visit_var(self, node):
        var_name = node.token.value
        var_value = self.scope.get(var_name)
        if var_value is None:
            raise ValueError(f"Unknown variable {var_name}")
        return var_value

    def visit_number(self, node):
        return float(node.token.value)

    def visit_unaryop(self, node):
        match node.op.value:
            case "-":
                return -self.visit(node.number)
            case "+":
                return self.visit(node.number)
            case _:
                raise ValueError("Invalid operator")

    def visit_binop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case _:
                raise ValueError("Invalid operator")

    def visit_block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.complex_statement)

    def visit_complex_statement(self, node):
        for child in node.children:
            self.visit(child)

    def eval(self, code):
        tree = self.parser.parse(code)
        self.visit(tree)
        return self.scope
