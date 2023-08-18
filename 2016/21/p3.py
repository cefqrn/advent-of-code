def rotate(l, amount):
    if amount < 0:
        for _ in range(-amount):
            l.append(l.pop(0))
    else:
        for _ in range(amount):
            l.insert(0, l.pop())

def rotate_letter_scramble(l, letter):
    xi = l.index(letter)
    xi += xi >= 4
    rotate(l, xi + 1)

def rotate_letter_unscramble(l, letter):
    xi = l.index(letter) or len(l)
    if not xi & 1:
        xi += len(l)
    
    rotate(l, -(xi // 2 + 1))
    # xi = [1, 1, 6, 2, 7, 3, 8, 4][l.index(letter)]
    # rotate(l, -xi)

def move_scramble(l, x, y):
    letter = l.pop(int(x))
    l.insert(int(y), letter)

def solve(initial, instructions, unscramble=False):
    if unscramble:
        rotate_letter = rotate_letter_unscramble
        move = lambda l, x, y: move_scramble(l, y, x)
        instructions = reversed(instructions)
    else:
        rotate_letter = rotate_letter_scramble
        move = move_scramble

    data = list(initial)
    for instruction in instructions:
        match instruction.split():
            case "swap", "position", x, "with", "position", y:
                x, y = int(x), int(y)
                data[x], data[y] = data[y], data[x]
            case "swap", "letter", x, "with", "letter", y:
                xi, yi = data.index(x), data.index(y)
                data[xi], data[yi] = y, x
            case "rotate", direction, x, "step" | "steps":
                direction = -1 if (direction == "left") ^ unscramble else 1
                rotate(data, direction * int(x))
            case "rotate", "based", "on", "position", "of", "letter", x:
                rotate_letter(data, x)
            case "reverse", "positions", x, "through", y:
                x = int(x)
                y = int(y)
                data[x:y+1] = reversed(data[x:y+1])
            case "move", "position", x, "to", "position", y:
                move(data, x, y)
    
    return "".join(data)

with open(0) as f:
    instructions = f.readlines()

print(
    solve("abcdefgh", instructions),
    solve("fbgdceah", instructions, unscramble=True)
)
