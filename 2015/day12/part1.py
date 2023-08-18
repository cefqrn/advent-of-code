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

import re
import json

print(sum(map(int, re.findall(r"-?[0-9]+", s))))

def hunt(obj):
    if isinstance(obj, dict):
        if "red" in obj.values():
            return 0
        obj = obj.values()

    s = 0
    for o in obj:
        if isinstance(o, int):
            s += o
            continue
        elif isinstance(o, str):
            continue
        
        s += hunt(o)
    
    return s

print(hunt(json.loads(s)))