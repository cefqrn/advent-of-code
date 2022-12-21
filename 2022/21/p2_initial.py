import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *

monkeys = {}
for line in lines:
    monkey, *yell = line.split()
    if monkey == "root:":
        monkeys[monkey[:-1]] = yell[0], '==', yell[2]
    else:
        monkeys[monkey[:-1]] = yell

def find_yell(monkey):
    yell = monkeys[monkey]
    
    try:
        return int(yell[0])
    except ValueError:
        return int(eval(f"{find_yell(yell[0])} {yell[1]} {find_yell(yell[2])}"))

paths = {}
def find_paths(start="root"):
    possible = [monkeys[start][0]]
    while possible:
        curr = possible.pop()
        yell = monkeys[curr]

        try:
            int(yell[0])
            continue
        except ValueError:
            paths[yell[0]] = curr
            paths[yell[2]] = curr
            possible.extend([yell[0], yell[2]])

find_paths()
possible = ["root"]
while possible

print(paths)