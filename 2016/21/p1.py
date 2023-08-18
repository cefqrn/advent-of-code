with open(0) as f:
    instructions = f.readlines()

# using a deque only allows popping at the ends
data = list("abcdefgh")
for i, instruction in enumerate(instructions):
    match instruction.split():
        case "swap", "position", x, "with", "position", y:
            xl = data[x := int(x)]
            yl = data[y := int(y)]
            data[x] = yl
            data[y] = xl
        case "swap", "letter", x, "with", "letter", y:
            xi = data.index(x)
            yi = data.index(y)
            data[xi] = y
            data[yi] = x
        case "rotate", direction, x, "step" | "steps":
            x = int(x)
            if direction == "left":
                for _ in range(x):
                    data.append(data.pop(0))
            else:
                for _ in range(x):
                    data.insert(0, data.pop())
        case "rotate", "based", "on", "position", "of", "letter", x:
            xi = data.index(x)
            xi += 1 + (xi >= 4)
            for _ in range(xi):
                data.insert(0, data.pop())
        case "reverse", "positions", x, "through", y:
            x = int(x)
            y = int(y)
            data[x:y+1] = reversed(data[x:y+1])
        case "move", "position", x, "to", "position", y:
            l = data.pop(int(x))
            data.insert(int(y), l)
    print(''.join(data))

print(''.join(data))
