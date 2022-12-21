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
    possible = [start]
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


def check_path(monkey, required):
    if monkey == "humn":
        return required

    m1, op, m2 = monkeys[monkey]
    
    if m1 in in_humn_path:
        p2 = find_yell(m2)
        if op == "-":
            NEEDED = required + p2
        elif op == "/":
            NEEDED = required * p2
        elif op == "*":
            NEEDED = required // p2
        elif op == "+":
            NEEDED = required - p2
        else:
            NEEDED = p2
        m = m1
    else:
        p1 = find_yell(m1)
        if op == "-":
            NEEDED = p1 - required
        elif op == "/":
            NEEDED = p1 // required
        elif op == "*":
            NEEDED = required // p1
        elif op == "+":
            NEEDED = required - p1
        else:
            NEEDED = p1
        m = m2
        
    return check_path(m, NEEDED)


curr = "humn"
in_humn_path = {curr}
while curr != "root":
    curr = paths[curr]
    in_humn_path.add(curr)

monkeys["humn"] = [int(monkeys["humn"][0])]

print(check_path("root", 1))
