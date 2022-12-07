# separate (57 + 61)
# print(sum(l[2]-87+(l[2]+~l[0])%3*3for l in open(0,'rb')))
# print(sum((l[0]+l[2]-1)%3+~-l[2]%3*3+1for l in open(0,'rb')))

# 54 + 58
print(sum(b-87+(b+~a)%3*3for a,_,b,_ in open(0,'rb')))
print(sum((a+b-1)%3+~-b%3*3+1for a,_,b,_ in open(0,'rb')))

# all in one* (91)
# print(sum(l[2]-87+(l[2]+~l[0])%3*3+1j*((l[0]+l[2]-1)%3+~-l[2]%3*3+1)for l in open(0,'rb')))
# alternatively ((a + b - 1) = (~-a + b))
# print(sum(l[2]-87+(l[2]+~l[0])%3*3+1j*((~-l[0]+l[2])%3+~-l[2]%3*3+1)for l in open(0,'rb')))

# 79
print(sum(b-87+(b+~a)%3*3+1j*((~-a+b)%3+~-b%3*3+1)for a,_,b,_ in open(0,'rb')))

# 78 by Crowthebird#2090
print(sum(b-87+(b+~a)%3*3-1j*~((~-a+b)%3+~-b%3*3)for a,_,b,_ in open(0,'rb')))


# *p1 is real, p2 is imaginary