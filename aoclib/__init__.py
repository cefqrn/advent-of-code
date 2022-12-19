__all__ = [
    'input_string', 'blocks', 'lines', 'lines_nonempty', 'lines_transposed',
    'lists', 'ints', 'floats'
]

from . import parsing
from . import grid

class _CouldNotOpenInputError(Exception): ...


def _get_input() -> str:
    from itertools import filterfalse

    # get the name of the file that imported this module
    _frame = next(filterfalse(lambda frame: frame.filename.startswith('<'), _stack()[2:]), None)
    if _frame is None:
        raise _CouldNotOpenInputError

    try:
        with open(_Path(_frame.filename).parent / "input") as f:
            input_string = f.read().rstrip('\n')
    except FileNotFoundError:
        raise _CouldNotOpenInputError

    return input_string


if __name__ != "__main__":
    from inspect import stack as _stack
    from pathlib import Path as _Path

    try:
        input_string = _get_input()
    except _CouldNotOpenInputError:
        print("Could not open input.")
        input_string = ""

    blocks           = parsing.get_blocks(input_string)
    lines            = parsing.get_lines(input_string)
    lines_nonempty   = parsing.get_lines_nonempty(input_string)
    lines_transposed = grid.transpose(lines)

    lists = parsing.get_lists(input_string)

    ints   = parsing.get_ints(input_string)
    floats = parsing.get_floats(input_string)
