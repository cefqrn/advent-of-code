with open("day06/input") as f:
    s = f.read().strip()

"""part 1"""

# from itertools import*
# l=[0]*10**6
# for c in s.split('\n'):
#     *_,o,a,_,b=c.split()
#     a,b=zip(map(int,a.split(',')),map(lambda x:x+1,map(int,b.split(','))))
#     for x,y in product(range(*a),range(*b)):
#         l[x*1000+y]=[(z:="fn".find(o[1])),not l[x*1000+y]][z<0]
# print(sum(l))

# from itertools import*
# l=[0]*10**6
# for c in s.split('\n'):
#     *_,o,a,_,b=c.split()
#     a,b=zip(map(int,a.split(',')),[x+1for x in map(int,b.split(','))])
#     for x,y in product(range(*a),range(*b)):
#         l[x*1000+y]=[(z:="fn".find(o[1])),not l[x*1000+y]][z<0]
# print(sum(l))

# from itertools import*
# f=str.split
# l=[0]*10**6
# for c in s.split('\n'):
#  *_,o,a,_,b=f(c)
#  for x,y in product(*starmap(range,zip(map(int,f(a,',')),[x+1for x in map(int,f(b,','))]))):l[x*1000+y]=[(z:="fn".find(o[1])),not l[x*1000+y]][z<0]
# print(sum(l))

# from itertools import*
# f=str.split
# l=[0]*10**6
# for c in s.split('\n'):
#  *_,o,a,_,b=f(c);o="fn".find(o[1]);*p,=zip([int(x)for x in f(a,',')],[x+1for x in map(int,f(b,','))])
#  for x,y in product(*starmap(range,p)):l[x*1000+y]=[o,not l[x*1000+y]][o<0]
# print(sum(l))

# from itertools import*
# f=str.split
# l={}
# for c in f(s,'\n'):
#  *_,o,a,_,b=f(c);o=~"of".find(o[1])
#  for p in product(*starmap(range,zip(map(int,f(a,',')),[x+1for x in map(int,f(b,','))]))):l[p]=not[o,l.get(p,0)][o]
# print(sum(l.values()))

# from itertools import*
# f=str.split
# l={}
# for c in f(s,'\n'):
#  *_,o,a,_,b=f(c);o=~"of".find(o[1])
#  for p in product(*starmap(range,zip(map(int,f(a,',')),map(lambda x:int(x)+1,f(b,','))))):l[p]=not[o,l.get(p,0)][o]
# print(sum(l.values()))

# from itertools import*
# f=str.split
# l={}
# for c in f(s,'\n'):
#  *_,o,a,_,b=f(c);o=~"of".find(o[1])
#  for p in product(*starmap(range,zip(eval(a),map(lambda x:x+1,eval(b))))):l[p]=not[o,l.get(p,0)][o]
# print(sum(l.values()))

# from itertools import*
# l={}
# for c in s.split('\n'):
#  *_,o,a,_,b=c.split();o=~"of".find(o[1])
#  for p in product(*starmap(range,zip(eval(a),map(lambda x:x+1,eval(b))))):l[p]=not[o,l.get(p,0)][o]
# print(sum(l.values()))

"""both parts"""

from itertools import*
l,m={},{}
for c in s.split('\n'):
 *_,o,a,_,b=c.split();o=~"of".find(o[1])
 for p in product(*starmap(range,zip(eval(a),[x+1for x in eval(b)]))):l[p]=not[o,l.get(p,0)][o];m[p]=max(0,m.setdefault(p,0)+(o+1or 2))
print(sum(l.values()),sum(m.values()))
