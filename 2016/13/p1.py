from heapq import heappop, heappush
number = 1358

def is_wall(x, y):
    value = x*x + 3*x + 2*x*y + y + y*y + number
    return sum(map(int, f"{value:b}")) & 1

target = 31,39
def h(x, y, cost):
    # return 0
    return abs(target[0] - x) + abs(target[1] - y) + cost

s = 0

p = 1, 1
possibilities = [(h(*p, 0), 0, p)]
costs = {p: 0}
while possibilities:
    _, cost, p = heappop(possibilities)
    x, y = p
    if p == target:
        print(cost)
        break

    ncost = cost + 1
    for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
        np = nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or is_wall(nx, ny):
            continue

        if (c:=costs.get(np)) is not None and c < ncost: continue
        costs[np] = ncost

        s += 1

        heappush(possibilities, (h(nx, ny, ncost), ncost, np))
print(s)