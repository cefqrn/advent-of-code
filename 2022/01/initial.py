# this was written before the library existed

import os

with open(os.path.join(os.path.dirname(__file__), "input")) as f:
    inputString = f.read()

elves = []
for elf in inputString.split('\n\n'):
    elves.append(sum(map(int, elf.split())))

elves.sort()
print(elves[-1])
print(sum(elves[-3:]))