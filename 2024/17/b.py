from itertools import groupby, product
from pathlib import Path

p1 = p2 = 0

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.splitlines()
sections = [
    list(section)
    for has_content, section in groupby(lines, bool)
    if has_content
]

from re import findall

a, b = sections

def batched(it, n):
    return list(zip(*n*[iter(it)]))

from functools import cache
from math import trunc

def run(program, a, b=0, c=0):
    registers = [a, b, c]

    def combo(operand):
        if operand > 3:
            return registers[operand-4]
        else:
            return operand

    output = []
    counter = 0
    while counter < len(program):
        opcode, operand = program[counter:counter+2]

        match opcode:
            case 0:
                registers[0] = trunc(registers[0] / 2**combo(operand))
            case 1:
                registers[1] = registers[1] ^ operand
            case 2:
                registers[1] = combo(operand) % 8
            case 3:
                if registers[0]:
                    counter = operand
                    continue
            case 4:
                registers[1] ^= registers[2]
            case 5:
                output.append(combo(operand) % 8)
            case 6:
                registers[1] = trunc(registers[0] / 2**combo(operand))
            case 7:
                registers[2] = trunc(registers[0] / 2**combo(operand))

        counter += 2

    return tuple(output)

@cache
def get_val(n):
    possible = []
    for a in range(1<<10):
        if (x := run(program, a)) and x[0] == n:
        # if (1 ^ (a%8) ^ (a >> ((a%8) ^ 2))) % 8 == n:
            possible += a,

    return possible

program = tuple(map(int, b[0].split(": ")[1].split(",")))

registers = list(map(int, findall(r"\d+", "".join(a))))
print(','.join(map(str, run(program, *registers))))

possible = set(get_val(program[-1]))
best = None
for i, needed in enumerate(program[:-1][::-1], 1):
    new_possible = set()
    for a in possible:
        if run(program, a)[-i:] == program[-i:]:
            new_possible.add(a)

    for a, b in product(possible, get_val(needed)):
        b_len = b.bit_length()
        new = (a << 3) | b
        if run(program, new)[-i:] == program[-i:]:
            new_possible.add(new)

    possible = new_possible
    for a in possible:
        output = run(program, a, 0, 0)

        if output != program:
            continue

        if best is None or best > a:
            best = a

print(best)
