"""
Q7 - Interactive Formula Validator with Custom Exceptions
Python 3.10+
"""
import re

class FormulaError(Exception):
    pass

class InvalidFormatError(FormulaError):
    pass

class UnknownVariableError(FormulaError):
    pass

class DivisionByZeroError(FormulaError):
    pass

class UnsupportedOperatorError(FormulaError):
    pass

NUMBER = r"(?:[+-]?(?:\d+(?:\.\d*)?|\.\d+))"
IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
TOKEN = re.compile(rf"^\s*({NUMBER}|{IDENT})\s*([+\-*/%])\s*({NUMBER}|{IDENT})\s*$")
ASSIGN = re.compile(rf"^\s*({IDENT})\s*=\s*({NUMBER})\s*$")

def to_number(token, variables):
    try:
        if re.fullmatch(NUMBER, token):
            return float(token)
    except ValueError:
        raise InvalidFormatError("Invalid numeric value.")

    if token in variables:
        return variables[token]
    raise UnknownVariableError(f"Unknown variable: {token}")

def format_number(value):
    if value == int(value):
        return str(int(value))
    return str(value)

def evaluate(line, variables):
    match = TOKEN.match(line)
    if not match:
        if re.search(r"//|\*\*|[<>^&|]", line):
            raise UnsupportedOperatorError("Only +, -, *, / and % are supported.")
        raise InvalidFormatError("Expected: operand operator operand.")

    left, op, right = match.groups()
    a = to_number(left, variables)
    b = to_number(right, variables)

    if op in {"/", "%"} and b == 0:
        raise DivisionByZeroError("Division by zero is not allowed.")

    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    if op == "%":
        return a % b

    raise UnsupportedOperatorError(f"Unsupported operator: {op}")

def main():
    variables = {}

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().lower() == "quit":
            break
        if not line.strip():
            continue

        try:
            assignment = ASSIGN.match(line)
            if assignment:
                name, value = assignment.groups()
                variables[name] = float(value)
                continue

            # A valid variable assignment with a formula is also accepted.
            if "=" in line:
                left, expr = line.split("=", 1)
                left = left.strip()
                if not re.fullmatch(IDENT, left):
                    raise InvalidFormatError("Invalid variable name.")
                value = evaluate(expr, variables)
                variables[left] = value
                continue

            result = evaluate(line, variables)
            print(format_number(result))

        except FormulaError as exc:
            print(type(exc).__name__)
            print(str(exc))

if __name__ == "__main__":
    main()
