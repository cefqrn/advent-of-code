with open("day05/input") as f:
    s = f.read()

# from re import findall as f
# print(len([l for l in s.split()if f(".*[aeiou]"*3,l)and f(r"(.)\1",l)and f("^(?!.*(ab|cd|pq|xy)).*",l)]))

import re
f=lambda*a:print(sum(all(map(re.search,a,[l]*len(a)))for l in s.split()))
f(".*[aeiou]"*3,r"(.)\1","(?!ab|cd|pq|xy)")
f(r"(..).*\1",r"(.).\1")