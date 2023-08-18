from collections.abc import Iterable, Mapping

directions: dict[str, tuple[int, int]] = {
    'U': ( 0, -1),
    'D': ( 0,  1),
    'L': (-2,  0),
    'R': ( 2,  0)
}


def get_code(keypad: str, instructions: Iterable[Iterable[str]], directions: Mapping[str, tuple[int, int]]=directions) -> str:
    keypad_lookup: dict[tuple[int, int], str] = {}
    position: tuple[int, int] | None = None
    for y, row in enumerate(keypad.splitlines()):
        for x, button in enumerate(row):
            if button.isspace():
                continue

            keypad_lookup[(x, y)] = button
            if button == '5':
                # set starting position to the position of the '5' button
                position = x, y

    if position is None:
        raise ValueError("keypad doesn't contain the '5' button")

    x, y = position
    output = ""
    for instruction in instructions:
        for direction in instruction:
            try:
                delta = directions[direction]
            except KeyError as e:
                raise ValueError(f"invalid direction: {direction}") from e
            
            dx, dy = delta
            new_position = x + dx, y + dy
            
            if keypad_lookup.get(new_position) is None:
                # ignore the instruction if it doesn't lead to a button
                continue
        
            x, y = position = new_position

        output += keypad_lookup[position]
    
    return output


p1_keypad = """
1 2 3
4 5 6
7 8 9
"""

p2_keypad = """
    1
  2 3 4
5 6 7 8 9
  A B C
    D
"""

with open(0) as f:
    instructions = f.read().split()
    
print(get_code(p1_keypad, instructions))
print(get_code(p2_keypad, instructions))
