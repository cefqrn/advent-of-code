from sys import setrecursionlimit

setrecursionlimit(400000 + 2)

def solve(row: int, mask: int, row_count: int, safe_count: int=0) -> int:
    if row_count <= 1:
        return safe_count + row.bit_count()
    
    left_safe  = (row >> 1) | ((mask + 1) >> 1)
    right_safe = (row << 1) | 1

    next_row = ~(left_safe ^ right_safe) & mask

    return solve(next_row, mask, row_count - 1, safe_count + row.bit_count())

with open(0) as f:
    row_str = f.read().strip()

row = int(row_str.translate(str.maketrans("^.", "01")), 2)
mask = 2**len(row_str) - 1

print(solve(row, mask, 40), solve(row, mask, 400000))
