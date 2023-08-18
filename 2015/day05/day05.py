with open("day05/input") as f:
    s = f.read()

p1 = 0
for l in s.strip().split('\n'):
    if any(map(lambda x: x in l, ['ab', 'cd', 'pq', 'xy'])):
        continue

    if sum(l.count(v) for v in'aeiou') < 3:
        continue

    for c1, c2 in zip(l, l[1:]):
        if c1 == c2:
            break
    else:
        continue

    p1 += 1

print(p1)