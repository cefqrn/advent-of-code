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

from collections import defaultdict
from re import compile, finditer

ELEMENT_PATTERN = compile(r"[A-Z][a-z]?")
ReplacementTable = dict[str, list[str]]
Molecule = dict[str, int]

elements_string, molecule_string = s.split('\n\n')

elements: ReplacementTable = defaultdict(list)
for e in elements_string.splitlines():
    element, product_string = e.split(" => ")
    elements[element].append(product_string)

products = set()
molecule = defaultdict(int)
for m in finditer(ELEMENT_PATTERN, molecule_string):
    element = m.group()
    for product_string in elements[element]:
        products.add(molecule_string[:m.start()] + product_string + molecule_string[m.end():])

print(len(products))