"""
Q1 - Campus Merit Analyzer using Compound Data Structures
"""
from collections import defaultdict

n, k, m = map(int, input().split())

# semester -> list of student tuples
students = defaultdict(list)

# subject -> maximum mark and corresponding enrollments
subject_top = [{"mark": -1, "enrollments": []} for _ in range(m)]

for _ in range(n):
    data = input().split()
    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])
    marks = list(map(int, data[4:]))

    avg = sum(marks) / m

    # Store as tuple: (enrollment, name, cpi, average, marks)
    students[semester].append(
        (enrollment, name, cpi, avg, marks)
    )

    # Find subject-wise toppers
    for i, mark in enumerate(marks):
        if mark > subject_top[i]["mark"]:
            subject_top[i]["mark"] = mark
            subject_top[i]["enrollments"] = [enrollment]
        elif mark == subject_top[i]["mark"]:
            subject_top[i]["enrollments"].append(enrollment)

for semester in sorted(students):
    # Higher CPI -> higher average marks -> smaller enrollment
    students[semester].sort(
        key=lambda x: (-x[2], -x[3], x[0])
    )

    top_k = students[semester][:k]
    enrollments = [student[0] for student in top_k]

    print(f"Semester {semester}: {' '.join(enrollments)}")

# Subject-wise toppers
for i in range(m):
    toppers = sorted(subject_top[i]["enrollments"])
    print(f"S{i + 1}: {' '.join(toppers)}")
