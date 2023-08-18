from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)


from collections import deque
import operator

operations = {
    "AND": operator.and_,
    "OR":  operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift
}


def solve(inp: str, b: int | None = None):
    values = {'b': b}

    def get_value(id: str):
        if (v:=values.get(id)) is None:
            return int(id)
        return v

    instructions = deque(inp.strip().split('\n'))
    while (instructions):
        instruction = instructions.popleft()
        inputs, output = instruction.split(' -> ')

        if output == 'b' and values.get('b') is not None:
            continue
        
        inputs = inputs.split()

        try:
            if len(inputs) == 3: # binary operation
                a = get_value(inputs[0])
                b = get_value(inputs[2])

                values[output] = operations[inputs[1]](a, b)
            elif len(inputs) == 2: # unary operation (always not)
                values[output] = ~get_value(inputs[1])
            else: # const
                values[output] = get_value(inputs[0])
        except ValueError as e:
            instructions.append(instruction)

    return values["a"]


from time import perf_counter
st = perf_counter()

p1 = solve(s)
print(f'p1: {p1}')
print(f'p2: {solve(s, p1)}')

print(f'done in {perf_counter() - st:.5f} s')

import 