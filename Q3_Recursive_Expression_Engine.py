"""
Q3 - Recursive Expression Engine with Memoization
Supports non-negative integer literals, +, -, *, parentheses and variables.
Python 3.10+
"""
import re
import sys
sys.setrecursionlimit(1_000_000)

NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

class InvalidExpression(Exception):
    pass

class CycleDetected(Exception):
    pass

class Parser:
    def __init__(self, text, resolver):
        self.text = text
        self.i = 0
        self.resolver = resolver

    def skip(self):
        while self.i < len(self.text) and self.text[self.i].isspace():
            self.i += 1

    def parse(self):
        value = self.expression()
        self.skip()
        if self.i != len(self.text):
            raise InvalidExpression()
        return value

    def expression(self):
        value = self.term()
        while True:
            self.skip()
            if self.i >= len(self.text) or self.text[self.i] not in "+-":
                return value
            op = self.text[self.i]
            self.i += 1
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs

    def term(self):
        value = self.factor()
        while True:
            self.skip()
            if self.i >= len(self.text) or self.text[self.i] != "*":
                return value
            self.i += 1
            value *= self.factor()

    def factor(self):
        self.skip()
        if self.i >= len(self.text):
            raise InvalidExpression()

        ch = self.text[self.i]

        if ch.isdigit():
            start = self.i
            while self.i < len(self.text) and self.text[self.i].isdigit():
                self.i += 1
            return int(self.text[start:self.i])

        if ch == "(":
            self.i += 1
            value = self.expression()
            self.skip()
            if self.i >= len(self.text) or self.text[self.i] != ")":
                raise InvalidExpression()
            self.i += 1
            return value

        match = NAME.match(self.text, self.i)
        if match:
            name = match.group()
            self.i = match.end()
            return self.resolver(name)

        raise InvalidExpression()

def main():
    v = int(input().strip())
    if not 1 <= v <= 200000:
        raise ValueError("Invalid variable count.")

    definitions = {}
    for _ in range(v):
        line = input()
        if "=" not in line:
            raise ValueError("Invalid variable definition.")
        name, expr = line.split("=", 1)
        name = name.strip()
        if not NAME.fullmatch(name):
            raise ValueError("Invalid variable name.")
        definitions[name] = expr

    target = input()

    memo = {}
    active = set()

    def evaluate_variable(name):
        if name not in definitions:
            raise InvalidExpression()
        if name in memo:
            return memo[name]
        if name in active:
            raise CycleDetected()

        active.add(name)
        try:
            value = Parser(definitions[name], evaluate_variable).parse()
            memo[name] = value
            return value
        finally:
            active.remove(name)

    try:
        answer = Parser(target, evaluate_variable).parse()
        print(answer)
    except CycleDetected:
        print("CYCLE")
    except (InvalidExpression, RecursionError):
        print("INVALID")

if __name__ == "__main__":
    main()
