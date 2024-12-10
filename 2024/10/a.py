from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

grid = {}
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        try:
            grid[x, y] = int(c)
        except ValueError:
            grid[x, y] = 999

w, h = len(line), len(lines)

directions = (0, -1), (1, 0), (0, 1), (-1, 0)

def solve(p1):
    result = 0
    for (ix, iy), height in grid.items():
        if height != 0:
            continue

        remaining = [(ix, iy, height)]
        seen = set()
        while remaining:
            x, y, height = remaining.pop()
            for dx, dy in directions:
                nx, ny = x+dx, y+dy
                if (nx, ny) not in grid: continue

                nheight = grid[nx, ny]
                if nheight != height + 1:
                    continue

                if p1:
                    if (nx, ny) in seen: continue
                    seen.add((nx, ny))

                if nheight == 9:
                    result += 1
                    continue


                remaining.append((nx, ny, nheight))

    return result

print(solve(True))
print(solve(False))
