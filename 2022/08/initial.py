import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

s = 0
for i, line in enumerate(lines):
    for j, tree in enumerate(line):
        if max(line[:j] or [chr(1)]) < tree or max(line[j+1:] or [chr(1)]) < tree:
            s += 1
            continue
        
        try:
            if max(list(zip(*lines))[j][:i] or [chr(1)]) < tree:
                s += 1
                continue
        except:
            pass
        
        try:
            if max(list(zip(*lines))[j][i+1:] or [chr(1)]) < tree:
                s += 1
                continue
        except:
            pass

print(s)

s = 0
best = 0
for i, line in enumerate(lines):
    for j, tree in enumerate(line):
        right = 0
        for t in line[j+1:]:
            right += 1
            if t >= tree:
                break

        left = 0
        for t in line[:j][::-1]:
            left += 1
            if t >= tree:
                break

        top = 0
        for t in list(zip(*lines))[j][i+1:]:
            top += 1
            if t >= tree:
                break

        bottom = 0
        for t in list(zip(*lines))[j][:i][::-1]:
            bottom += 1
            if t >= tree:
                break

        curr = right * left * top * bottom

        if curr > best:
            best = curr

print(best)
