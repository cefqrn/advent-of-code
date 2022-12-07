import os
import sys

sys.path.append(os.path.join(sys.path[0], '../..'))

from aoc_library import *

class File:
    def __init__(self, size, name):
        self.size = size
        self.name = name

class Directory:
    def __init__(self, parent, name):
        self.parent = parent
        self.children: list[Directory | File] = []
        self.name = name

    @property
    def size(self):
        s = 0
        for child in self.children:
            s += child.size
        return s

root = Directory(None, "/")
current_dir = root
for i, command in enumerate(lines[1:]):
    if not command.startswith("$"):
        continue

    match command.split()[1:]:
        case ["cd", ".."]:
            current_dir = current_dir.parent
            continue
        case ["cd", new_dir]:
            for child in current_dir.children:
                if child.name == new_dir:
                    current_dir = child
                    break
            continue
        case ["ls"]:
            i += 1
            while i < len(lines) and not lines[i + 1].startswith("$"):
                try:
                    a, b  = lines[i+1].split()
                except ValueError:
                    break

                if a == "dir":
                    new_dir = Directory(current_dir, b)
                    current_dir.children.append(new_dir)
                else:
                    current_dir.children.append(File(int(a), b))

                i+=1

directories = [root]
to_check = [root]
while to_check:
    curr = to_check.pop()
    for child in curr.children:
        if isinstance(child, Directory):
            to_check.append(child)
            directories.append(child)

s = sum(y.size for y in filter(lambda x: x.size <= 100000, directories))

print(s)

s = 70000000
directories.sort(key=lambda x: x.size)

s -= directories[-1].size

for directory in directories:
    if s + directory.size >= 30000000:
        print(directory.size)
        break
