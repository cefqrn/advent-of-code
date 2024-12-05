from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

a, b = sections

a = [tuple(map(int, x.split("|"))) for x in a.split()]
b = tuple(map(eval, b.split()))

def is_incorrect(pages):
    for x, y in a:
        try:
            if pages.index(x) > pages.index(y):
                return pages.index(x), pages.index(y)
        except:
            continue

    return False

incorrect = []
for pages in b:
    if is_incorrect(pages):
        incorrect.append(pages)
    else:
        p1 += pages[len(pages) // 2]

for pages in map(list, incorrect):
    while z := is_incorrect(pages):
        i, j = z
        pages[i], pages[j] = pages[j], pages[i]

    p2 += pages[len(pages) // 2]

print(p1)
print(p2)
