with open(0) as f:
    input_str = f.read()

def is_triangle(triangle):
    a, b, c = sorted(triangle)
    return a + b > c

p1 = len(list(filter(is_triangle, zip(*3*[iter(map(int, input_str.split()))]))))
from itertools import chain
p2 = len(list(filter(is_triangle, chain(*map(lambda x: zip(*(map(int, l.split()) for l in x)), zip(*3*[iter(input_str.splitlines())]))))))

print(p1, p2)
