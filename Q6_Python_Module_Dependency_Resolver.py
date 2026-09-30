"""
Q6 - Python Module Dependency Resolver
Kahn's algorithm + min-heap for lexicographically smallest valid order.
Python 3.10+
"""
import heapq
from collections import defaultdict

def find_cycle(graph, modules):
    color = {u: 0 for u in modules}  # 0=unvisited, 1=active, 2=done
    stack = []
    position = {}

    def dfs(u):
        color[u] = 1
        position[u] = len(stack)
        stack.append(u)

        for v in graph[u]:
            if color[v] == 0:
                result = dfs(v)
                if result:
                    return result
            elif color[v] == 1:
                start = position[v]
                return stack[start:] + [v]

        stack.pop()
        position.pop(u, None)
        color[u] = 2
        return None

    for u in sorted(modules):
        if color[u] == 0:
            result = dfs(u)
            if result:
                return result
    return []

def main():
    n, e = map(int, input().split())
    modules = [input().strip() for _ in range(n)]
    module_set = set(modules)

    graph = defaultdict(set)
    indegree = {m: 0 for m in modules}

    for _ in range(e):
        a, b = input().split()
        if a not in module_set or b not in module_set:
            raise ValueError("Import edge contains an unknown module.")

        # a imports b => b must load before a.
        if b not in graph[a]:
            graph[a].add(b)
            indegree[a] += 1

    # Reverse graph: dependency -> modules that depend on it.
    dependents = defaultdict(list)
    for a, deps in graph.items():
        for b in deps:
            dependents[b].append(a)

    heap = [m for m in modules if indegree[m] == 0]
    heapq.heapify(heap)
    order = []

    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in dependents[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(heap, v)

    if len(order) == n:
        print(*order)
    else:
        cycle = find_cycle(graph, modules)
        print("CYCLE")
        print(*cycle)

if __name__ == "__main__":
    main()
