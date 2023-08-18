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

s = s.strip()  # s is the input as a string

def parse_instruction(instruction):
    instruction, params = instruction.split(' ', 1)
    params = params.split(', ')
    for i, param in enumerate(params):
        try:
            params[i] = int(param)
        except ValueError:
            pass

    return instruction, params

program = tuple(map(parse_instruction, s.splitlines()))

def run(a_val):
    registers = {
        "a": a_val,
        "b": 0
    }

    pc = 0
    while True:
        i, params = program[pc]

        if i == "hlf":
            registers[params[0]] //= 2
        elif i == "tpl":
            registers[params[0]] *= 3
        elif i == "inc":
            registers[params[0]] += 1
        elif i == "jmp":
            pc += params[0] - 1
        elif i == "jie":
            pc += (params[1] - 1) * (registers[params[0]] % 2 == 0)
        elif i == "jio":
            pc += (params[1] - 1) * (registers[params[0]] == 1)

        pc += 1
        if pc >= len(program):
            break
    
    return registers["b"]

print(f"p1: {run(0)}")
print(f"p2: {run(1)}")