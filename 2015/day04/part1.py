import hashlib

s = "iwrupvqb"

for x in map(str, range(10_000_000)):
    if hashlib.md5((s+x).encode()).hexdigest().startswith("00000"):
        print(x)
        break

import hashlib

key = "iwrupvqb"
suffix = 0

while True:
    prehash = key+str(suffix)
    hash = hashlib.md5(prehash.encode()).hexdigest()
    if hash[:6] == '000000': break
    suffix += 1

print(suffix)