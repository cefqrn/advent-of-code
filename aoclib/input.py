from . import parsing
from . import grid

from itertools import filterfalse

__all__ = [
    "input_string", "blocks", "lines", "lines_nonempty", "lines_transposed",
    "lists", "ints", "floats"
]


class CouldNotOpenInputError(Exception): ...


def _get_input() -> str:
    from inspect import stack as stack
    from pathlib import Path

    # get the name of the file that imported this module
    frame = next(filterfalse(lambda frame: frame.filename.startswith('<'), stack()[2:]), None)
    if frame is None:
        raise CouldNotOpenInputError

    try:
        with open(Path(frame.filename).parent / "input") as f:
            input_string = f.read().rstrip('\n')
    except FileNotFoundError:
        raise CouldNotOpenInputError

    return input_string


if __name__ != "__main__":
    try:
        input_string = _get_input()
    except CouldNotOpenInputError:
        print("Could not open input.")
        input_string = ""

    blocks           = parsing.get_blocks(input_string)
    lines            = parsing.get_lines(input_string)
    lines_nonempty   = parsing.get_lines_nonempty(input_string)
    lines_transposed = grid.transpose(lines)

    lists = parsing.get_lists(input_string)

    ints   = parsing.get_ints(input_string)
    floats = parsing.get_floats(input_string)
