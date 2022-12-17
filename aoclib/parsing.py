from re import findall

input_string = ""


def get_chunks(s: str, chunk_count: int) -> list[tuple[str, ...]]:
    return list(zip(*chunk_count*[iter(get_lines(s))]))


def get_blocks(s: str) -> list[str]:
    return s.split('\n\n')


def get_lines(s: str) -> list[str]:
    return s.splitlines()


def get_lines_nonempty(s: str) -> list[str]:
    return list(filter(None, get_lines(s)))


def get_ints(s: str) -> list[int]:
    return list(map(int, findall(r"[+-]?\d+", s)))


def get_floats(s: str) -> list[float]:
    return list(map(float, findall(r"[+-]?\d*\.?\d+", s)))


def get_lists(s: str) -> list[list]:
    return list(map(str.split, get_lines_nonempty(s)))
