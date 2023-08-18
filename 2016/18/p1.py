SAFE = 1
TRAP = 0

row_count = 400000

def next_row(row):
    new_row = []
    padded_row = [SAFE, *row, SAFE]
    for a, b, c in zip(padded_row, padded_row[1:], padded_row[2:]):
        if (not a and not b and c) or (a and not b and not c) or (not a and b and c) or (a and b and not c):
            new_row.append(TRAP)
        else:
            new_row.append(SAFE)
    return new_row

def print_row(row):
    for t in row:
        print(end="^."[t])
    print()

with open(0) as f:
    row = f.read().strip()

row = *map(".".__eq__, row),

p1 = sum(row)
for _ in range(row_count-1):
    row = next_row(row)
    # print_row(row)
    p1 += sum(row)

print(p1)
