from re import search

with open(0) as f:
    ips = f.readlines()

p1 = p2 = 0
for ip in ips:
    if search(r"(\w)(?!\1)(\w)\2\1", ip) and not search(r"(\w)(?!\1)(\w)\2\1[^\[]*\]", ip):
        p1 += 1

    if search(r"(?:^|\])[^\[]*(\w)(?!\1)(\w)\1.*\[[^\]]*\2\1\2|(\w)(?!\3)(\w)\3[^\[]*\].*\4\3\4[^\]]*(?:$|\[)", ip):
        p2 += 1

print(p1, p2)
