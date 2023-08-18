def solve(instructions, registers):
    instruction_count = len(instructions)
    pc = 0
    instructions = instructions.copy()
    while pc < instruction_count:
        if pc == 4:
            registers["a"] += registers["b"] * registers["d"]
            registers["c"] = 0
            registers["d"] = 0
            pc += 5

        match instructions[pc].split():
            case "cpy", x, y:
                if y not in registers:
                    pc += 1
                    continue

                x = registers[x] if x in registers else int(x)
                registers[y] = x
            case "inc", x:
                if x in registers:
                    registers[x] += 1
            case "dec", x:
                if x in registers:
                    registers[x] -= 1
            case "jnz", x, y:
                x = registers[x] if x in registers else int(x)
                if x != 0:
                    y = registers[y] if y in registers else int(y)
                    pc += y - 1
            case "tgl", x:
                x = registers[x] if x in registers else int(x)
                if not 0 <= (tp := pc + x) < instruction_count:
                    pc += 1
                    continue

                t = instructions[tp]
                match t.split():
                    case "inc", x:
                        instructions[tp] = f"dec {x}"
                    case _, x:
                        instructions[tp] = f"inc {x}"
                    case "jnz", x, y:
                        instructions[tp] = f"cpy {x} {y}"
                    case _, x, y:
                        instructions[tp] = f"jnz {x} {y}"

        pc += 1
    
    return registers['a']

with open(0) as f:
    instructions = f.readlines()

print(solve(instructions, dict(zip("abcd", [7] + [0]*3))))
print(solve(instructions, dict(zip("abcd", [12] + [0]*3))))
