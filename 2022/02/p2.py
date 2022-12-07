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

    if b == 0:
        s += (a - 1) % 3 + 1
    if b == 1:
        s += a + 3 + 1
    if b == 2:
        s += (a + 1) % 3 + 6 + 1
    
print(s)
