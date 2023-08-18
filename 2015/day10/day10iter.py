from itertools import tee
from time import perf_counter

s = "1113122113"

def iterate(s):
    count = 1
    prev = next(s)
    
    for n in s:
        if prev == n:
            count += 1
        else:
            yield f'{count}'
            yield prev
            prev = n
            count = 1

    yield f'{count}'
    yield prev

st = perf_counter()

s = iter(s)
for i in range(50):
    s = iterate(s)
    if i == 39:
        s, s1 = tee(s)

        print(f'p1: {len(list(s1))} in {perf_counter() - st:.2f} s')

print(f'p2: {len(list(s))} in {perf_counter() - st:.2f} s')
