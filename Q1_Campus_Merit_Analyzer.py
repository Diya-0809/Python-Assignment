"""
Q1 - Campus Merit Analyzer using Compound Data Structures
Problem Statement: You are given records of students in the form enrollment, name, semester, CPI and a list of subject marks. Build a
program that stores the records using lists, tuples and dictionaries. For each semester, print the top K students by CPI. If CPI is the
same, prefer the student with higher average marks; if still tied, prefer lexicographically smaller enrollment number. Also print the
subject-wise topper for every subject code.
"""
from collections import defaultdict

def main():
    first = input().split()
    if len(first) != 3:
        raise ValueError("First line must contain n, k and m.")
    n, k, m = map(int, first)
    if not (1 <= n <= 100000 and 1 <= k <= 50 and 1 <= m <= 12):
        raise ValueError("n, k or m is outside the allowed range.")

    # tuple: (enrollment, name, semester, cpi, marks)
    students = []
    by_semester = defaultdict(list)

    for _ in range(n):
        parts = input().split()
        if len(parts) != 4 + m:
            raise ValueError("Each student row must contain 4 fields plus m marks.")
        enrollment, name = parts[0], parts[1]
        semester = int(parts[2])
        cpi = float(parts[3])
        marks = tuple(map(int, parts[4:]))

        if not (1 <= semester <= 8 and 0 <= cpi <= 10):
            raise ValueError("Invalid semester or CPI.")
        if any(not 0 <= x <= 100 for x in marks):
            raise ValueError("Marks must be between 0 and 100.")

        student = (enrollment, name, semester, cpi, marks)
        students.append(student)
        by_semester[semester].append(student)

    # Higher CPI, then higher average marks, then lexicographically smaller enrollment.
    def student_key(s):
        enrollment, _, _, cpi, marks = s
        return (-cpi, -sum(marks) / len(marks), enrollment)

    for semester in sorted(by_semester):
        ranked = sorted(by_semester[semester], key=student_key)
        print(f"Semester {semester}:", *[s[0] for s in ranked[:k]])

    # Subject-wise topper(s): all students tied at the maximum mark.
    for j in range(m):
        best = max(s[4][j] for s in students)
        toppers = sorted(s[0] for s in students if s[4][j] == best)
        print(f"S{j + 1}:", *toppers)

if __name__ == "__main__":
    main()
