from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

from re import findall

enabled = True

def do():
    global enabled
    enabled = True

def don_t():
    global enabled
    enabled = False

def mul(a, b):
    global p1, p2

    p1 += a*b
    p2 += a*b * enabled

for call in findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", contents):
    exec(call.replace("'", "_"))

print(p1, p2)
