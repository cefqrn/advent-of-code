import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

input_string = get_input()

S = "abcdefghijklmnopqrstuvwxyz"
S += S.upper()

s = 0
# lines wasn't set by the library when this was written (this is what got it into there)
for l in get_lines():
    length = len(l)
    s += S.index((set(l[:length//2]) & set(l[length//2:])).pop()) + 1
print(s)

s=0
for x, y, z in zip(get_lines()[::3], get_lines()[1::3], get_lines()[2::3]):
    s+= S.index((set(x) & set(y) & set(z)).pop())+ 1

print(s)
