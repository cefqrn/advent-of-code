with open(0) as f:
    block_list = f.readlines()

p1 = None

ip_count = 0
prev_hi = -1
for lo, hi in sorted(tuple(map(int, block.split("-"))) for block in block_list):
    if lo > prev_hi + 1:
        ip_count += lo - prev_hi - 1
        if p1 is None:
            p1 = prev_hi + 1

    prev_hi = max(prev_hi, hi)

ip_count += 2**32 - prev_hi - 1

print(p1, ip_count)
