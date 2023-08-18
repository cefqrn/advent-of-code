def next_row(row: int, mask: int) -> int:
    left_safe  = (row >> 1) | ((mask + 1) >> 1)
    right_safe = (row << 1) | 1

    return ~(left_safe ^ right_safe) & mask
    # return (left_safe ^ right_safe ^ mask) & mask

def solve(row: int, mask: int, row_count: int) -> int:
    safe_count = row.bit_count()
    for _ in range(row_count-1):
        row = next_row(row, mask)
        safe_count += row.bit_count()

    return safe_count

with open(0) as f:
    row_str = f.read().strip()

row = int(row_str.translate(str.maketrans("^.", "01")), 2)
mask = 2**len(row_str) - 1

print(solve(row, mask, 40), solve(row, mask, 400000))
