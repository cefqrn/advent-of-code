import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from aoclib.input import *
from aoclib.parsing import *


monkeys = {}
for line in lines:
    monkey, *yell = line.split()
    monkeys[monkey[:-1]] = yell

def find_yell(monkey):
    yell = monkeys[monkey]
    try:
        return int(yell[0])
    except ValueError:
        return int(eval(f"{find_yell(yell[0])} {yell[1]} {find_yell(yell[2])}"))

print(find_yell("root"))
