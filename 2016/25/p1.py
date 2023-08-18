from itertools import cycle, count
from operator import ne

def solve(instructions):
    instruction_count = len(instructions)

    for i in count():
        pc = 0
        output = bytearray()
        registers = dict(zip("abcd", [i, 0, 0, 0]))
        while pc < instruction_count:
            match instructions[pc].split():
                case "cpy", x, y:
                    if x.isdigit():
                        registers[y] = int(x)
                    else:
                        registers[y] = registers[x]
                case "inc", x:
                    registers[x] += 1
                case "dec", x:
                    registers[x] -= 1
                case "jnz", x, y:
                    if x.isdigit() and int(x) != 0 or x in registers and registers[x] != 0:
                        pc += int(y) - 1
                case "out", x:
                    output.append(registers[x] if x in registers else int(x))
                    if any(map(ne, output, cycle([0, 1]))):
                        break
                    if len(output) > 2000:
                        return i

            pc += 1

with open(0) as f:
    instructions = f.readlines()

print(solve(instructions))
