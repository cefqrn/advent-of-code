with open("day05/input") as f:
    s = f.read()

p2 = 0
for l in s.strip().split('\n'):
    for c1, c2, c3 in zip(l, l[1:], l[2:]):
        if c1 == c3:
            break
    else:
        continue

    for c1, c2 in zip(l, l[1:]):
        if l.count(c1+c2)-1:
            break
    else:
        continue

    p2 += 1

print(p2)