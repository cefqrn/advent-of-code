from collections import deque
from itertools import count
from hashlib import md5

salt = "ngcjuoqr"

def get_streak(digest, streak_length):
    for window in zip(*(digest[x:] for x in range(streak_length))):
        if len(set(window)) == 1:
            return window[0]

def get_64th_key(stretch_count):
    def hash_(i: int):
        digest = md5(f"{salt}{i}".encode()).hexdigest()
        for _ in range(stretch_count):
            digest = md5(digest.encode()).hexdigest()
        return digest
    
    hashes = deque()

    quintuples = {}
    for i in range(1000):
        digest = hash_(i)
        hashes.append(digest)
        if c := get_streak(digest, 5):
            quintuples[c] = i

    key_count = 0
    for i in count():
        digest1 = hashes.popleft()
        hashes.append(digest2 := hash_(i + 1000))

        if c := get_streak(digest2, 5):
            quintuples[c] = i + 1000
        
        if c := get_streak(digest1, 3):
            if quintuples.get(c, 0) > i:
                key_count += 1
                if key_count == 64:
                    return i

print(get_64th_key(0), get_64th_key(2016))
