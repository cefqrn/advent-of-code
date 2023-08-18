from re import search, finditer

with open(0) as f:
    ips = f.readlines()

# ips = ["aba[bab]xyz", "xyx[xyx]xyx", "aaa[kek]eke", "zazbz[bzb]cdb"]

def supports_ssl(s):
    supernet = [""]
    hypernet = [""]
    in_hypernet = False
    for c in s:
        if c == "[":
            in_hypernet = True
            supernet.append("")
            continue
        if c == "]":
            in_hypernet = False
            hypernet.append("")
            continue

        if in_hypernet:
            hypernet[-1] += c
        else:
            supernet[-1] += c
    
    for supernet_string in supernet:
        for m in finditer(r"(\w)(?=(?!\1)(\w)\1)", supernet_string):
            a, b = m.groups()
            for hypernet_string in hypernet:
                if (b+a+b) in hypernet_string:
                    return True
    
    return False

p1 = p2 = 0
for ip in ips:
    if search(r"(\w)(?!\1)(\w)\2\1", ip) and not search(r"\[[^\]]*(\w)(?!\1)(\w)\2\1[^\[]*\]", ip):
        p1 += 1

    if supports_ssl(ip):
        p2 += 1

print(p1, p2)
