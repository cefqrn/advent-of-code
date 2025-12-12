# https://github.com/smontanaro/python-0.9.1/
# https://github.com/smontanaro/python-0.9.1/blob/main/lib/string.py
# https://github.com/smontanaro/python-0.9.1/blob/main/lib/testall.py

import string

def sum(amounts):
    result = 0
    for x in amounts:
        result = result + x
    
    return result

def parse(line):
    region = string.splitfields(line, ': ')
    
    dimensions = string.splitfields(region[0], 'x')
    width, height = eval(dimensions[0]), eval(dimensions[1])
    
    amounts = []
    for amount in string.split(region[1]):
        amounts.append(eval(amount))
    
    return (width, height), amounts

def multiply_positive(a, b):
    # avoid creating range in memory
    product = 0
    while a:
        product = product + b
        a = a - 1
    
    return product

f = open('input', 'r')

data = f.read(65536)
sections = string.splitfields(string.strip(data), '\n\n')

shapes = sections[:-1]
regions = sections[-1:][0]  # negative indices on slices but not get

result = 0
regions = string.splitfields(regions, '\n')
for line in regions:
    (width, height), amounts = parse(line)
    
    # (width/3) * (height/3) overflows?
    tile_count = multiply_positive(width/3, height/3)
    required_tile_count = sum(amounts)
    
    if required_tile_count <= tile_count:
        result = result + 1

print result
