from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input"

contents = INPUT_FILE.read_text().rstrip()
lines = contents.split("\n")
sections = contents.split("\n\n")

p1 = p2 = 0

def batched(it, n):
    return list(zip(*n*[iter(it)]))

from itertools import repeat

free_count = 0
file_count = 0
curr = 0

file_spots = []
free_spots = []

curr_id = 0
disk = []
for file, free in batched(map(int, contents + '0'), 2):
    disk += repeat(curr_id, int(file))
    disk += '.' * free

    file_spots.append((curr, file, curr_id))

    curr += file
    free_spots.append((curr, free))

    curr += free

    file_count += file
    free_count += free

    curr_id += 1

disk_p1 = disk.copy()
for _ in range(free_count):
    while (c := disk_p1.pop()) == '.':
        pass

    try:
        disk_p1[disk_p1.index('.')] = c
    except:
        disk_p1.append(c)

for i, x in enumerate(disk_p1):
    if x == '.':
        continue

    p1 += i*int(x)

from bisect import insort_left
for file_pos, taken, file_id in reversed(file_spots):
    for i, (pos, free) in enumerate(free_spots):
        if file_pos < pos: break  # find way to use takewhile
        if free < taken: continue

        free_spots[i] = (pos + taken, free - taken)
        disk[pos:pos+taken] = repeat(file_id, taken)
        disk[file_pos:file_pos+taken] = repeat('.', taken)

        for i, (pos, free) in enumerate(free_spots):
            if pos + free == file_pos:
                free_spots[i] = (file_pos, free + taken)
                break
        else:
            insort_left(free_spots, (file_pos, taken))

        break

for i, x in enumerate(disk):
    if x == '.':
        continue

    p2 += i*int(x)

print(p1)
print(p2)
