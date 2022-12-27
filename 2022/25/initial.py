import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

values = '=-012'

s = 0
for num in lines:
    c = 0
    for digit in num:
        c *= 5
        c += values.index(digit) - 2

    s += c

print(s)

o = ""
while s:
    s, m = divmod(s + 2, 5)
    o = values[m] + o

print(o)
