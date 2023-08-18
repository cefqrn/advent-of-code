from functools import partial
from operator import not_, add

initial = "01111001100111011"

def process(x: bytes) -> bytes:
    return x + b"\0" + bytes(map(not_, x[::-1]))

def xnor(a, b):
    return not a ^ b

def checksum(x: bytes) -> bytes:
    output = x
    while not len(output) & 1:
        output = bytes(map(xnor, output[::2], output[1::2]))
        
    return bytes(map(partial(add, 48), output))

def solve(required_length: int) -> bytes:
    data = bytes(map(int, initial))
    while len(data) < required_length:
        data = process(data)

    return checksum(data[:required_length])

print(solve(272), solve(35651584))
