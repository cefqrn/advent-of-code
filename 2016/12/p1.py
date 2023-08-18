def solve(instructions, registers):
    instruction_count = len(instructions)
    pc = 0

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
                if x.isdigit() and int(x) != 0 or registers[x] != 0:
                    pc += int(y) - 1

        pc += 1
    
    return registers['a']

with open(0) as f:
    instructions = f.readlines()

print(solve(instructions, dict(zip("abcd", [0] * 4))))
print(solve(instructions, dict(zip("abcd", [0, 0, 1, 0]))))
