with open(0) as f:
    x = f.read().strip()

from collections import deque

directions = deque([1, 1j, -1, -1j])
seen = {pos:=0}

p2 = None
for direction, *distance in x.split(', '):
    directions.rotate((direction == 'R') * 2 - 1)
    for i in range(int(''.join(distance))):
        pos += directions[0]
        if p2 is None and pos in seen:
            p2 = int(abs(pos.real) + abs(pos.imag))

        seen.add(pos)

print(f"p1: {int(abs(pos.real) + abs(pos.imag))}")
print(f"p2: {p2}")
