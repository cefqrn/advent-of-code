import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

input_string = get_input()

other_scores = "ABC"
my_scores = "XYZ"

s = 0
for line in input_string.split('\n'):
    a, b = line.split()
    a = other_scores.index(a)
    b = my_scores.index(b)

    s += b + 1

    if a == b:
        s += 3
        continue
    
    if a == 0:
        if b == 1:
            s += 6
            continue
        if b == 2:
            continue
    
    if a == 1:
        if b == 2:
            s += 6
            continue
        if b == 0:
            continue
    
    if a == 2:
        if b == 0:
            s += 6
            continue
        if b == 1:
            continue
    
print(s)
