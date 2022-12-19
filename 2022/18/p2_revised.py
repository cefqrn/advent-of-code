NEIGHBORS = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

g = set(map(eval, open(0)))

s = 0
remaining = [(-1, -1, -1)]
visited = set()
while remaining:
    x, y, z = remaining.pop()

    for dx, dy, dz in NEIGHBORS:
        n = x+dx, y+dy, z+dz

        for c in n:
            if c < -1 or c > 25:
                break
        else:
            if n in g:
                s += 1
            else:
                if n in visited:
                    continue
                
                visited.add(n)
                remaining.append(n)
    
print(s)
