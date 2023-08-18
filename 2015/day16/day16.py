from __future__ import annotations

from sys import stdin, argv
from os import isatty

if len(argv) == 2:
    with open(argv[1]) as f:
        s = f.read()
elif not isatty(0):  # check if stdin is a file
    s = stdin.read()
else:
    print("input not given")
    exit(1)

s = s.strip()  # s is the input as a string

import re

card_details = {"children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3, "akitas": 0, "vizslas": 0, "goldfish": 5, "trees": 3, "cars": 2, "perfumes": 1}

def p1_check(details):
    for detail_type, detail_count in details.items():
        if detail_count != card_details[detail_type]:
            return False
    return True

def p2_check(details):
    for detail_type, detail_count in details.items():
        match detail_type:
            case "cats" | "trees":
                if detail_count <= card_details[detail_type]:
                    return False
            case "pomeranians" | "goldfish":
                if detail_count >= card_details[detail_type]:
                    return False
            case _:
                if detail_count != card_details[detail_type]:
                    return False
    return True

for l in s.splitlines():
    sue, details = l.split(': ', 1)
    sue = int(sue[4:])

    details = eval('{' + re.sub(r'([a-z]+)', r'"\1"', details) + '}')

    if p1_check(details):
        print(f"p1: {sue}")
    if p2_check(details):
        print(f"p2: {sue}")
