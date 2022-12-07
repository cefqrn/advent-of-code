from pathlib import Path
from bisect import insort


def delete(path: Path):
    if path.is_dir():
        for child in path.iterdir():
            delete(child)

        path.rmdir()
    else:
        path.unlink()


root = Path(__file__).parent / "root"

if root.exists():
    delete(root)

root.mkdir()
current_dir = root

with open(0) as f:
    lines = f.readlines()

for i, command in enumerate(lines):
    if not command.startswith("$"):
        continue

    match command.split()[1:]:
        case ["cd", path]:
            if path == "/":
                current_dir = root
            else:
                current_dir = (current_dir / path).resolve()
        case ["ls"]:
            i += 1
            while i < len(lines) and not lines[i].startswith("$"):
                try:
                    a, b  = lines[i].split()
                except ValueError:
                    break

                if a == "dir":
                    (current_dir / b).mkdir()
                else:
                    with open(current_dir / b, "w") as f:
                        f.write("a" * int(a))

                i+=1


def get_size(path: Path):
    if path.is_dir():
        return sum(f.stat().st_size for f in path.glob("**/*") if f.is_file())

    return path.stat().st_size


p1 = 0

to_check = [root]
sizes = []
while to_check:
    folder = to_check.pop()
    to_check.extend(filter(Path.is_dir, folder.iterdir()))

    size = get_size(folder)
    insort(sizes, size)
    if size <= 100000:
        p1 += size

print(p1)

space = 70000000 - sizes[-1]
for size in sizes:
    if space + size >= 30000000:
        print(size)
        break
