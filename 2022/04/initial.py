import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

s = 0
for l in lines:
    a, b = l.split(',')
    *a, = map(int, a.split('-'))
    *b, = map(int, b.split('-'))

    if b[0] == a[0]:
        s += 1
        continue
    if b[1] == a[1]:
        s += 1
        continue

    if b[0] < a[0]:
        a, b = b, a
    s += b[1] <= a[1]
    
print(s)


s = 0
for l in lines:
    a, b = l.split(',')
    *a, = map(int, a.split('-'))
    *b, = map(int, b.split('-'))

    a = set(range(a[0], a[1] + 1))
    b = set(range(b[0], b[1] + 1))

    s += bool(a & b)
    
print(s)