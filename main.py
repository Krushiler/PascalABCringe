from interpreter import Interpreter
import sys

if __name__ == "__main__":
    interp = Interpreter()
    with open('code.pabinge', 'r') as f:
        code = f.read()
    try:
        print(interp.eval(code))
    except (SyntaxError, ValueError, TypeError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
