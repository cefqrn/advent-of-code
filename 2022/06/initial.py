import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

for i, l in enumerate(input_string):
    if len(set(input_string[i:i+4])) == 4:
        print(i+4)
        break

for i, l in enumerate(input_string):
    if len(set(input_string[i:i+14])) == 14:
        print(i+14)
        break