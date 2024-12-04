from itertools import product
from re import finditer, M

def iter_len(it):
    return sum(1 for _ in it)

with open(0) as f:
    contents = f.read()

line_length = contents.index("\n")

print(sum(
        iter_len(finditer(
            f"(?=(.|\n){{{distance}}}".join(string) + ")"*(len(string)-1),
            contents,
            M
        ))
        for distance, string in product(
            (0, line_length, line_length+1, line_length-1),
            ("XMAS", "SAMX")
        )
    ), sum(
        iter_len(finditer(
            f"(?<={a}(.|\n){{{line_length-1}}})A(?=(.|\n){{{line_length-1}}}{b})",
            contents,
            M
        ))
        for a, b in (
            ("M.M", "S.S"),
            ("S.M", "S.M"),
            ("S.S", "M.M"),
            ("M.S", "M.S"),
        )
    )
)
