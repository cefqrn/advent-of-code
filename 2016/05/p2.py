from contextlib import suppress
from hashlib import md5

door_id = b"reyedfim%d"
p1 = ""
p2 = [''] * 8

i = 0
while not all(p2):
    digest = md5(door_id % i).digest()
    i += 1

    if any(digest[:2]) or digest[2] & 0xf0:
        continue

    if len(p1) < 8:
        p1 += f"{digest[2] & 0xf:x}"
    
    with suppress(ValueError, IndexError):
        if not p2[j:=digest[2] & 0x0f]:
            p2[j] = f"{digest[3] >> 4:x}"

    print(p1.ljust(8, '*'), "".join(c if c else '*' for c in p2), end='\r')

print(p1, "".join(p2))
