"""
Q3 - Recursive Expression Engine with Memoization
"""
import sys

sys.setrecursionlimit(1_000_000)

v = int(input())

definitions = {}

for _ in range(v):
    line = input().strip()

    if "=" not in line:
        continue

    name, expr = line.split("=", 1)
    name = name.strip()
    expr = expr.strip()

    definitions[name] = expr

target = input().strip()

class Parser:
    def __init__(self, text, resolve_variable):
        self.text = text
        self.n = len(text)
        self.pos = 0
        self.resolve_variable = resolve_variable

    def skip_spaces(self):
        while self.pos < self.n and self.text[self.pos].isspace():
            self.pos += 1

    def parse(self):
        self.skip_spaces()

        if self.pos >= self.n:
            raise ValueError("Invalid expression")

        value = self.parse_expression()

        self.skip_spaces()

        # Extra characters mean invalid syntax
        if self.pos != self.n:
            raise ValueError("Invalid expression")

        return value

    def parse_expression(self):
        value = self.parse_term()

        while True:
            self.skip_spaces()

            if self.pos >= self.n:
                break

            op = self.text[self.pos]

            if op not in "+-":
                break

            self.pos += 1
            right = self.parse_term()

            if op == "+":
                value += right
            else:
                value -= right

        return value

    def parse_term(self):
        value = self.parse_factor()

        while True:
            self.skip_spaces()

            if self.pos >= self.n or self.text[self.pos] != "*":
                break

            self.pos += 1
            right = self.parse_factor()

            value *= right

        return value

    def parse_factor(self):
        self.skip_spaces()

        if self.pos >= self.n:
            raise ValueError("Invalid expression")

        ch = self.text[self.pos]

        # Parenthesized expression
        if ch == "(":
            self.pos += 1

            value = self.parse_expression()

            self.skip_spaces()

            if self.pos >= self.n or self.text[self.pos] != ")":
                raise ValueError("Missing ')'")

            self.pos += 1
            return value

        # Non-negative integer
        if ch.isdigit():
            start = self.pos

            while self.pos < self.n and self.text[self.pos].isdigit():
                self.pos += 1

            return int(self.text[start:self.pos])

        # Variable name
        if ch.isalpha() or ch == "_":
            start = self.pos

            while (
                self.pos < self.n
                and (self.text[self.pos].isalnum() or self.text[self.pos] == "_")
            ):
                self.pos += 1

            name = self.text[start:self.pos]

            return self.resolve_variable(name)

        raise ValueError("Invalid character")

state = {}
memo = {}

CYCLE = False


def evaluate_variable(name):
    global CYCLE

    # Undefined variable
    if name not in definitions:
        raise ValueError("Undefined variable")

    # Already calculated
    if state.get(name, 0) == 2:
        return memo[name]

    # Currently on recursion stack => cycle
    if state.get(name, 0) == 1:
        CYCLE = True
        raise RuntimeError("CYCLE")

    state[name] = 1

    try:
        parser = Parser(definitions[name], evaluate_variable)
        value = parser.parse()

        memo[name] = value
        state[name] = 2

        return value

    except RuntimeError:
        raise

    except Exception:
        raise ValueError("Invalid expression")

try:
    parser = Parser(target, evaluate_variable)
    answer = parser.parse()

    if CYCLE:
        print("CYCLE")
    else:
        print(answer)

except RuntimeError:
    print("CYCLE")

except Exception:
    print("INVALID")
