with open(0) as f:
    data = f.readlines()

for possible_chars in zip(*data):
    print(end=max(set(possible_chars), key=possible_chars.count))
    
for possible_chars in zip(*data):
    print(end=min(set(possible_chars), key=possible_chars.count))
