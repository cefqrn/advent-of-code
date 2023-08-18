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

# print(*map(sum,[[len(l)-len(eval(l)),l.count('"')+l.count('\\')+2]for l in s.strip().split()]))

# print(*map(sum,[[len(l)-len(eval(l)),sum(map(l.count,'"\\'))+2]for l in s.strip().split()]))

# z=s.split()
# print(sum(len(l)-len(eval(l))for l in z),sum(sum(map(l.count,'"\\'))+2for l in z))

a=b=0
for l in s.split():a+=len(l)-len(eval(l));b+=sum(map(l.count,'"\\'))+2
print(a,b)

z=s.split()
print(sum(len(l)-len(eval(l))for l in z),sum(map(s.count,'"\\'))+len(z)*2)