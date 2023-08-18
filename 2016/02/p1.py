with open(0) as f:
    instructions = f.read().split()

p1_codes = {
    (0, 2): "1",
    (1, 2): "2",
    (2, 2): "3",
    (0, 1): "4",
    (1, 1): "5",
    (2, 1): "6",
    (0, 0): "7",
    (1, 0): "8",
    (2, 0): "9",
}

p2_codes = {
    ( 0,  2): "1",
    (-1,  1): "2",
    ( 0,  1): "3",
    ( 1,  1): "4",
    (-2,  0): "5",
    (-1,  0): "6",
    ( 0,  0): "7",
    ( 1,  0): "8",
    ( 2,  0): "9",
    (-1, -1): "A",
    ( 0, -1): "B",
    ( 1, -1): "C",
    ( 0, -2): "D"
}

p1 = p2 = ""
x1 = y1 = 0
x2 = -2
y2 =  0

for instruction in instructions:
    for dir in instruction:
        prev1 = x1, y1
        prev2 = x2, y2

        x2 += (dir == 'R') - (dir == 'L')
        y2 += (dir == 'U') - (dir == 'D')
        x1 += (dir == 'R') - (dir == 'L')
        y1 += (dir == 'U') - (dir == 'D')

        if abs(x2) + abs(y2) > 2:
            x2, y2 = prev2

        if not 0 <= x1 <= 2 or not 0 <= y1 <= 2:
            x1, y1 = prev1

    p1 += p1_codes[(x1, y1)]
    p2 += p2_codes[(x2, y2)]

print(p1, p2)