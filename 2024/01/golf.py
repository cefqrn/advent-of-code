m,n=map(sorted,zip(*[map(int,l.split())for l in open(0)]))
p=q=0
for a,b in zip(m,n):q+=m.count(b)*b;p+=abs(a-b)
print(p,q)

# m,n=map(sorted,zip(*[map(int,l.split())for l in open(0)]))
# q=0
# print(sum((q:=q+m.count(b)*b)and abs(a-b)for a,b in zip(m,n)),q)

# l=[[*map(int,l.split())]for l in open(0)]
# p=q=0
# for a,b in l:q+=l[::2].count(b)*b;p+=abs(a-b)
# print(p,q)
