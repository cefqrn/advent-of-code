from string import ascii_lowercase
from re import compile

ROOM_PATTERN = compile(r"([a-z\-]+)-(\d+)\[([a-z]+)\]")

with open(0) as f:
    rooms = f.readlines()

p1 = p2 = 0
for room in rooms:
    name, sector_id, checksum = ROOM_PATTERN.match(room).groups()
    sector_id = int(sector_id)

    expected_checksum = ''.join(sorted(set(filter(str.isalpha, name)), key=lambda x: (-name.count(x), x))[:5])
    if checksum == expected_checksum:
        p1 += sector_id

    decrypted_name = name.translate(str.maketrans(ascii_lowercase + '-', ascii_lowercase[sector_id%26:] + ascii_lowercase[:sector_id%26] + ' '))

    if "north" in decrypted_name and "pole" in decrypted_name:
        print(f"{decrypted_name}: {sector_id}")

print(f"{p1 = }")
