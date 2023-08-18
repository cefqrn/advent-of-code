from heapq import heappop, heappush
number = 1358

def is_wall(x, y):
    value = x*x + 3*x + 2*x*y + y + y*y + number
    return sum(map(int, f"{value:b}")) & 1

pos = 1, 1
possibilities = [(0, *pos)]
costs = {pos: 0}
while possibilities:
    _, cost, x, y = heappop(possibilities)
    if cost == 50:
        continue

    for dx, dy in (0, 1), (1, 0), (0, -1), (-1, 0):
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or is_wall(nx, ny):
            continue

        if (c:=costs.get((nx, ny))) is not None and c <= cost + 1:
            continue
        costs[(nx, ny)] = cost + 1

        heappush(possibilities, (h(nx, ny), cost + 1, nx, ny))
print(len(costs))