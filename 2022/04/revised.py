import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

p1 = p2 = 0
for l in lines:
    a, b = l.split(',')
    *a, = map(int, a.split('-'))
    *b, = map(int, b.split('-'))

    a = set(range(a[0], a[1] + 1))
    b = set(range(b[0], b[1] + 1))

    p1 += len(a & b) == min(len(a), len(b))
    p2 += bool(a & b)
    
print(p1, p2)
