from itertools import product, starmap

with open("day06/input") as f:
    s = f.read()

lights1 = [[0]*1000 for _ in range(1000)]
lights2 = [[0]*1000 for _ in range(1000)]

# lights1 = [0]*1000000
# lights2 = [0]*1000000

area = lambda p1, p2: product(*starmap(range, zip([int(x) for x in p1.split(',')], [int(x)+1 for x in p2.split(',')])))

def on(coords):
    for x, y in coords:
        lights1[x][y] = 1
        lights2[x][y] += 1

def off(coords):
    for x, y in coords:
        lights1[x][y] = 0
        lights2[x][y] = (t:=lights2[x][y]) and t - 1
        # if lights2[x][y]:
            # lights2[x][y] -= 1

def toggle(coords):
    for x, y in coords:
        lights1[x][y] = not lights1[x][y]
        lights2[x][y] += 2

instructions = {
    "on": on,
    "off": off,
    "toggle": toggle
}

commands = s.strip().split('\n')
for command in commands:
    *_, c, p1, _, p2 = command.split()

    instructions[c](area(p1, p2))

print(f'p1: {sum(map(sum, lights1))}')
print(f'p2: {sum(map(sum, lights2))}')

# print(f'p1: {sum(lights1)}')
# print(f'p2: {sum(lights2)}')