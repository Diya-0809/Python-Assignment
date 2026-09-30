"""
Q6 - Python Module Dependency Resolver
"""
import heapq
import sys

sys.setrecursionlimit(1_000_000)

n, e = map(int, input().split())

modules = []

for _ in range(n):
    modules.append(input().strip())

module_set = set(modules)

# module -> integer index
index = {name: i for i, name in enumerate(modules)}

graph = [[] for _ in range(n)]
indegree = [0] * n

# Ignore duplicate edges
edges = set()

for _ in range(e):
    a, b = input().split()

    # a imports b => b -> a
    u = index[b]
    v = index[a]

    if (u, v) not in edges:
        edges.add((u, v))
        graph[u].append(v)
        indegree[v] += 1

heap = []

for i in range(n):
    if indegree[i] == 0:
        heapq.heappush(heap, modules[i])

order = []

while heap:
    current_name = heapq.heappop(heap)
    current = index[current_name]

    order.append(current_name)

    for nxt in graph[current]:
        indegree[nxt] -= 1

        if indegree[nxt] == 0:
            heapq.heappush(heap, modules[nxt])

if len(order) == n:
    print(" ".join(order))
    sys.exit(0)

color = [0] * n

parent = [-1] * n

cycle = None

for start in range(n):

    if color[start] != 0:
        continue

    # (node, next-neighbor-index)
    stack = [(start, 0)]
    color[start] = 1

    while stack and cycle is None:
        node, next_index = stack[-1]

        if next_index == len(graph[node]):
            color[node] = 2
            stack.pop()
            continue

        neighbor = graph[node][next_index]

        # Advance the neighbor index
        stack[-1] = (node, next_index + 1)

        if color[neighbor] == 0:
            parent[neighbor] = node
            color[neighbor] = 1
            stack.append((neighbor, 0))

        elif color[neighbor] == 1:
           
            cycle_nodes = [neighbor]

            current = node

            while current != neighbor:
                cycle_nodes.append(current)
                current = parent[current]

            cycle_nodes.append(neighbor)

            cycle_nodes.reverse()
            cycle = cycle_nodes

    if cycle is not None:
        break

print("CYCLE")
print(" ".join(modules[i] for i in cycle))
