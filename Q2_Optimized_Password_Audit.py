"""
Q2 - Optimized Password Audit with Pattern Constraints
"""
from collections import deque

class AhoCorasick:
    def __init__(self, words):
        self.next = [{}]
        self.fail = [0]
        self.output = [False]

        for word in words:
            node = 0
            for ch in word.lower():
                if ch not in self.next[node]:
                    self.next[node][ch] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.output.append(False)
                node = self.next[node][ch]
            self.output[node] = True

        q = deque()
        for child in self.next[0].values():
            q.append(child)

        while q:
            u = q.popleft()
            for ch, v in self.next[u].items():
                q.append(v)
                f = self.fail[u]
                while f and ch not in self.next[f]:
                    f = self.fail[f]
                self.fail[v] = self.next[f].get(ch, 0)
                self.output[v] = self.output[v] or self.output[self.fail[v]]

    def contains_banned(self, text):
        node = 0
        for ch in text.lower():
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            if self.output[node]:
                return True
        return False

def has_required_pattern(password):
    return (
        any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in "$#@" for c in password)
    )

def repeated_more_than_three(password):
    if not password:
        return False
    run = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            run += 1
            if run > 3:
                return True
        else:
            run = 1
    return False

def main():
    b = int(input().strip())
    if not 1 <= b <= 10000:
        raise ValueError("Invalid number of banned words.")

    banned = [input().rstrip("\n") for _ in range(b)]
    if any(not word for word in banned):
        raise ValueError("Banned words cannot be empty.")

    automaton = AhoCorasick(banned)

    n = int(input().strip())
    if not 1 <= n <= 100000:
        raise ValueError("Invalid number of passwords.")

    for i in range(1, n + 1):
        password = input().rstrip("\n")

        if not 6 <= len(password) <= 12:
            result = "WEAK_LENGTH"
        elif automaton.contains_banned(password):
            result = "COMPROMISED"
        elif repeated_more_than_three(password) or not has_required_pattern(password):
            result = "WEAK_PATTERN"
        else:
            result = "STRONG"

        print(f"{i}: {result}")

if __name__ == "__main__":
    main()
