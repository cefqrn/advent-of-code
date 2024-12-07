from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

from itertools import starmap
from operator import mul
from re import findall, sub

def solve(s):
    return sum(starmap(mul, map(eval, findall(r"mul\((\d{1,3},\d{1,3})\)", s))))

print(solve(contents))
print(solve(sub(r"don't\(\)(.|\n)*?(do\(\)|$)", "", contents)))
