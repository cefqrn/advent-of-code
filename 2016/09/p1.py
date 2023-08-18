def decompress(s):
    iter_s = iter(s)

    output = ""
    for c in iter_s:
        if c != '(':
            output += c
            continue

        a = b = 0
        while (c:=next(iter_s)) != 'x':
            a = a*10 + ord(c) - 48
        while (c:= next(iter_s)) != ')':
            b = b*10 + ord(c) - 48
        
        repeated = ''
        for _ in range(a):
            repeated += next(iter_s)
        
        output += b * decompress(repeated)
    
    return output

from functools import cache
@cache
def decompression_len(s):
    iter_s = iter(s)

    output = 0
    for c in iter_s:
        if c != '(':
            output += 1
            continue

        a = b = 0
        while (c:=next(iter_s)) != 'x':
            a = a*10 + ord(c) - 48
        while (c:= next(iter_s)) != ')':
            b = b*10 + ord(c) - 48
        
        repeated = ''
        for _ in range(a):
            repeated += next(iter_s)
        
        output += b * decompression_len(repeated)
    
    return output


# print(decompression_len("(27x12)(20x12)(13x14)(7x10)(1x12)A"))
with open(0) as f:
    print(decompression_len(f.read().strip()))
