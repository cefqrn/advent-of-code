from itertools import zip_longest
from time import perf_counter

s = "1113122113"

def iterate(s):
    count = 1
    o = []

    for c, n in zip_longest(s, s[1:]):
        if c == n:
            count += 1
        else:
            o.append(f'{count}' + c)
            count = 1
    
    return ''.join(o)
        
st = perf_counter()

for i in range(50):
    s = iterate(s)
    if i == 39:
        print(f'p1: {len(s)} in {perf_counter() - st:.2f} s')

print(f'p2: {len(s)} in {perf_counter() - st:.2f} s')