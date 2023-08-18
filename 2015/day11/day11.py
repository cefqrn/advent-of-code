from string import ascii_lowercase
s = "cqjxjnds"

PASSWORD_LENGTH = len(s)
BANNED = list(map(ascii_lowercase.index, "iol"))

def increment(s):
    for i in range(len(s)-1, -1, -1):
        if s[i] < len(ascii_lowercase) - 1:
            s[i] += 1
            return
        s[i] = 0

def has_straight(p):
    for a, b, c in zip(p, p[1:], p[2:]):
        if a == b - 1 == c - 2:
            return True

    return False

def has_pairs(p):
    has_pair = False
    i = 0

    while i < PASSWORD_LENGTH - 1:
        if p[i] == p[i + 1]:
            if has_pair:
                return True

            has_pair = True
            i += 1
        i += 1

    return False

def has_no_invalid_chars(p):
    return not any(map(p.__contains__, BANNED))

def is_valid(p):
    return has_straight(p) and has_pairs(p) and has_no_invalid_chars(p)


p = list(map(ascii_lowercase.index, s))

while not is_valid(p): increment(p)

print(f"p1: {''.join(map(ascii_lowercase.__getitem__, p))}")

increment(p)
while not is_valid(p): increment(p)

print(f"p2: {''.join(map(ascii_lowercase.__getitem__, p))}")
