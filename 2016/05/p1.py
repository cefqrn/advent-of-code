from contextlib import suppress
from hashlib import md5

door_id = b"reyedfim"
p1 = ""
p2 = [''] * 8

i = 0
while not all(p2):
    hex_digest = md5(door_id + str(i).encode()).hexdigest()
    i += 1

    if not hex_digest.startswith("00000"):
        continue

    if len(p1) < 8:
        p1 += hex_digest[5]
    
    with suppress(ValueError, IndexError):
        if not p2[j:=int(hex_digest[5])]:
            p2[j] = hex_digest[6]

    print(p1.ljust(8, '*'), "".join(c if c else '*' for c in p2), end='\r')

print(p1, "".join(p2))
