from collections import defaultdict

s = 34000000

def p2():
    houses = defaultdict(int)
    for i in range(1,s):
        for j in range(1, 51):
            houses[i*j] += i*11
            if houses[i*j] >= s:
                return i*j

print(p2())
