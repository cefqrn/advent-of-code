# this one doesn't work

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

ZERO = None

from collections import defaultdict, deque

from functools import total_ordering

seen = defaultdict(int)
@total_ordering
class WOWINT:
    def __init__(self, val):
        global ZERO
        if val == 0:
            ZERO = self

        self.id = seen[val]
        seen[val] += 1
        self.value = val

    def __add__(self, other):
        return self.value + other

    def __gt__(self, other):
        return self.value > other
    
    def __eq__(self, other):
        return self.value == other
    
    def copy(self):
        return WOWINT(self.value)

ints = list(map(WOWINT, ints[:]))
l = ints[:]
for n in ints:
    index = l.index(n)
    l.remove(n)
    n_index = (n.value+index) % len(l)
    l.insert(n_index, n.copy())
    # print([x.value for x in l])

# [0, 1, 2, 3]
# [0, 1, 3]
# [1, 2,  3]


s=0
zero_index = l.index(ZERO)
for i in 1,2,3:
    s+=l[(zero_index+i*1000)%len(l)].value

print(s)

# not 8616
# not 4609
# not 9662
# not 13278
# not -6319
# not -6763
