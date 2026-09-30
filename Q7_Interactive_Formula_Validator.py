"""
Q7 - Interactive Formula Validator with Custom Exceptions
"""
import re

class FormulaError(Exception):
    """Base class for formula-related errors."""
    pass

class InvalidFormatError(FormulaError):
    pass

class UnknownVariableError(FormulaError):
    pass

class DivisionByZeroError(FormulaError):
    pass

class UnsupportedOperatorError(FormulaError):
    pass

class Calculator:

    def __init__(self):
        self.variables = {}

    def get_value(self, operand):

        # Integer or decimal
        try:
            return float(operand)
        except ValueError:
            pass

        # Variable
        if operand in self.variables:
            return self.variables[operand]

        raise UnknownVariableError(
            f"Unknown variable: {operand}"
        )

    def evaluate(self, left, operator, right):

        left_value = self.get_value(left)
        right_value = self.get_value(right)

        if operator not in {"+", "-", "*", "/", "%"}:
            raise UnsupportedOperatorError(
                f"Unsupported operator: {operator}"
            )

        if operator in {"/", "%"} and right_value == 0:
            raise DivisionByZeroError(
                "Division by zero is not allowed"
            )

        if operator == "+":
            return left_value + right_value

        elif operator == "-":
            return left_value - right_value

        elif operator == "*":
            return left_value * right_value

        elif operator == "/":
            return left_value / right_value

        elif operator == "%":
            return left_value % right_value

    def process(self, line):

        line = line.strip()

        if not line:
            raise InvalidFormatError("Empty formula")

    
        if "=" in line:

            parts = line.split("=")

            if len(parts) != 2:
                raise InvalidFormatError(
                    "Invalid assignment format"
                )

            variable = parts[0].strip()
            expression = parts[1].strip()

            # Python identifier rule
            if not variable.isidentifier():
                raise InvalidFormatError(
                    f"Invalid variable name: {variable}"
                )

            # Assignment of a single value/variable
            if re.fullmatch(
                r"[+-]?(?:\d+(?:\.\d*)?|\.\d+|[A-Za-z_]\w*)",
                expression
            ):
                value = self.get_value(expression)

            else:
                # Assignment containing a formula
                match = re.fullmatch(
                    r"\s*(\S+)\s*([+\-*/%]+)\s*(\S+)\s*",
                    expression
                )

                if not match:
                    raise InvalidFormatError(
                        "Invalid assignment expression"
                    )

                left, operator, right = match.groups()

                if operator not in {"+", "-", "*", "/", "%"}:
                    raise UnsupportedOperatorError(
                        f"Unsupported operator: {operator}"
                    )

                value = self.evaluate(
                    left,
                    operator,
                    right
                )

            self.variables[variable] = value
            return None
            
        match = re.fullmatch(
            r"\s*(\S+)\s*([+\-*/%]+)\s*(\S+)\s*",
            line
        )

        if not match:
            raise InvalidFormatError(
                "Expected: operand operator operand"
            )

        left, operator, right = match.groups()

        if operator not in {"+", "-", "*", "/", "%"}:
            raise UnsupportedOperatorError(
                f"Unsupported operator: {operator}"
            )

        return self.evaluate(
            left,
            operator,
            right
        )

calculator = Calculator()

while True:

    try:
        line = input().strip()

    except EOFError:
        break

    if line.lower() == "quit":
        break

    try:
        result = calculator.process(line)

        # Assignment does not print a result.
        if result is not None:

            # Print integer values without .0
            if result.is_integer():
                print(int(result))
            else:
                print(result)

    except FormulaError as e:
        print(type(e).__name__)

    except Exception as e:
        # Safety net: calculator should never terminate
        # because of a single malformed input.
        print(type(e).__name__)
