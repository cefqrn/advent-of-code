with open(0) as f:
    directions = f.read().rstrip().split(", ")

def odd(x):
    return x & 1

def even(x):
    return not x & 1

pos = 0, 0

r = 0
for a in directions:
    direction, distance = a[0], int(a[1:])

    if direction == 'R':
        r = (r - 1) % 4
    else:
        r = (r + 1) % 4

    if odd(r):
        pos = pos[0] + (r-2)*distance, pos[1]
    else:
        pos = pos[0], pos[1] + (r-1)*distance

print(sum(map(abs, pos)), pos)
