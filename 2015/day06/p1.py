with open("day06/input") as f:
    s = f.read()

lights = []
for _ in range(1000):
    lights.append([0] * 1000)

commands = s.split('\n')

for command in commands:
    match command.split():
        case ["turn", "on", p1, _, p2]:
            x1, y1, x2, y2 = *map(int, p1.split(',')), *map(int, p2.split(','))
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    lights[x][y] = 1
        case ["turn", "off", p1, _, p2]:
            x1, y1, x2, y2 = *map(int, p1.split(',')), *map(int, p2.split(','))
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    lights[x][y] = 0
        case ["toggle", p1, _, p2]:
            x1, y1, x2, y2 = *map(int, p1.split(',')), *map(int, p2.split(','))
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    lights[x][y] = not lights[x][y]

print(sum(map(sum, lights)))