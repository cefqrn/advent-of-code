with open(0) as f:
    instructions = f.readlines()

data = list("fbgdceah")
for instruction in reversed(instructions):
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
                    data.insert(0, data.pop())
            else:
                for _ in range(x):
                    data.append(data.pop(0))
        case "rotate", "based", "on", "position", "of", "letter", x:
            xi = [1, 1, 6, 2, 7, 3, 8, 4][data.index(x)]
            for _ in range(xi):
                data.append(data.pop(0))
        case "reverse", "positions", x, "through", y:
            x = int(x)
            y = int(y)
            data[x:y+1] = reversed(data[x:y+1])
        case "move", "position", x, "to", "position", y:
            l = data.pop(int(y))
            data.insert(int(x), l)
    print(''.join(data))

print(''.join(data))
