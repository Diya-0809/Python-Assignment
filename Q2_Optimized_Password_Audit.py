"""
Q2 - Optimized Password Audit with Pattern Constraints
"""
from collections import deque

#  Trie Node 
class Node:
    def __init__(self):
        self.children = {}
        self.fail = 0
        self.output = False


#  Build Trie 
b = int(input())

trie = [Node()]

for _ in range(b):
    word = input().strip().lower()

    current = 0

    for ch in word:
        if ch not in trie[current].children:
            trie[current].children[ch] = len(trie)
            trie.append(Node())

        current = trie[current].children[ch]

    trie[current].output = True


#  Build Failure Links 
queue = deque()

# Root's direct children
for child in trie[0].children.values():
    trie[child].fail = 0
    queue.append(child)

while queue:
    current = queue.popleft()

    for ch, child in trie[current].children.items():
        queue.append(child)

        failure = trie[current].fail

        while failure != 0 and ch not in trie[failure].children:
            failure = trie[failure].fail

        if ch in trie[failure].children:
            trie[child].fail = trie[failure].children[ch]
        else:
            trie[child].fail = 0

        # If failure state represents a banned word,
        # this state also represents a banned word.
        trie[child].output |= trie[trie[child].fail].output


#  Password Validation 
n = int(input())

for index in range(1, n + 1):
    password = input().rstrip("\n")

    # 1. Length check
    if len(password) < 6 or len(password) > 12:
        print(f"{index}: WEAK_LENGTH")
        continue

    # 2. Pattern check
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False
    repeated = False

    previous = None
    count = 0

    for ch in password:
        if ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch.isdigit():
            has_digit = True
        elif ch in "$#@":
            has_special = True

        # Same character more than 3 times consecutively
        if ch == previous:
            count += 1
        else:
            previous = ch
            count = 1

        if count > 3:
            repeated = True

    if not (has_lower and has_upper and has_digit and has_special) or repeated:
        print(f"{index}: WEAK_PATTERN")
        continue

    # 3. Check banned words using Aho-Corasick
    current = 0
    compromised = False

    for ch in password.lower():
        while current != 0 and ch not in trie[current].children:
            current = trie[current].fail

        if ch in trie[current].children:
            current = trie[current].children[ch]
        else:
            current = 0

        if trie[current].output:
            compromised = True
            break

    if compromised:
        print(f"{index}: COMPROMISED")
    else:
        print(f"{index}: STRONG")
