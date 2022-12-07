import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *


b1, b2 = blocks

stacks = [''.join(m).strip()[-2::-1] for m in zip(*b1.split('\n'))][1::4]

for l in filter(None, b2.split('\n')):
    _, a, _, b, _, c = l.split()
    a,b,c = map(int, [a, b, c])

    stacks[c-1]+=stacks[b-1][-a:][::-1]
    stacks[b-1]=stacks[b-1][:-a]

print(''.join(stack[-1] for stack in stacks))


b1, b2 = blocks

stacks = [''.join(m).strip()[-2::-1] for m in zip(*b1.split('\n'))][1::4]

for l in filter(None, b2.split('\n')):
    _, a, _, b, _, c = l.split()
    a,b,c = map(int, [a, b, c])

    stacks[c-1]+=stacks[b-1][-a:]
    stacks[b-1]=stacks[b-1][:-a]

print(''.join(stack[-1] for stack in stacks))
