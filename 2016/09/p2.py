from functools import cache

@cache
def decompression_len(s, p2=False):
    iter_s = iter(s)

    output = 0
    for c in iter_s:
        if c != '(':
            output += 1
            continue

        a = b = 0
        while (c:=next(iter_s)) != 'x':
            a = a*10 + ord(c) - 48
        while (c:=next(iter_s)) != ')':
            b = b*10 + ord(c) - 48
        
        repeated = ''
        for _ in range(a):
            repeated += next(iter_s)
        
        output += b * decompression_len(repeated, p2) if p2 else b * len(repeated)
    
    return output

with open(0) as f:
    text = f.read().strip()

print(decompression_len(text), decompression_len(text, p2=True))
