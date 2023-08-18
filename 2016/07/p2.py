from itertools import groupby
from re import search, finditer

def supports_ssl(s):
    nets = [[], []]
    current_group = 0
    for i, group in groupby(s, "][".find):
        if i != -1:
            current_group = i
            continue

        nets[current_group].append("".join(group))

    supernet, hypernet = nets
    
    for supernet_string in supernet:
        # use lookahead to allow for overlap
        for m in finditer(r"(\w)(?=(?!\1)(\w)\1)", supernet_string):
            a, b = m.groups()
            for hypernet_string in hypernet:
                if (b+a+b) in hypernet_string:
                    return True
    
    return False

with open(0) as f:
    ips = f.readlines()

p1 = p2 = 0
for ip in ips:
    if search(r"(\w)(?!\1)(\w)\2\1", ip) and not search(r"(\w)(?!\1)(\w)\2\1[^\[]*\]", ip):
        p1 += 1

    if supports_ssl(ip):
        p2 += 1

print(p1, p2)
