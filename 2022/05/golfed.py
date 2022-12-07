# all of these work if there is a trailing newline

# 317
# from copy import*
# x,y=open(0).read().split('\n\n')
# p={int(n):s[::-1]for *s,n in[''.join(m).strip()for m in zip(*x.split('\n'))][1::4]}
# q=deepcopy(p)
# def f(d,o):
#  for l in y.splitlines():a,b,c=map(int,l.split()[1::2]);d[c].extend(d[b][-a:][::o]);d[b][-a:]=[]
#  print(*[s.pop()for s in d.values()],sep='')
# f(p,-1)
# f(q,1)

# 269
# x,y=open(0).read().split('\n\n')
# p=[''.join(m).strip()[-2::-1]for m in zip(*x.split('\n'))][1::4]
# q=p.copy()
# def f(d,o):
#  for l in y.splitlines():a,b,c=map(int,l.split()[1::2]);d[c-1]+=d[b-1][-a:][::o];d[b-1]=d[b-1][:-a]
#  print(*[s[-1]for s in d],sep='')
# f(p,-1)
# f(q,1)

# 267
# g=str.split
# x,y=g(open(0).read(),'\n\n')
# p=[''.join(m).strip()[-2::-1]for m in zip(*g(x,'\n'))][1::4]
# q=p.copy()
# def f(d,o):
#  for l in y.splitlines():a,b,c=map(int,g(l)[1::2]);d[c-1]+=d[b-1][-a:][::o];d[b-1]=d[b-1][:-a]
#  print(''.join(s[-1]for s in d))
# f(p,-1)
# f(q,1)

# 264 by Starwort#6129
# g=str.split
# I='\n'
# x,y=g(open(0).read(),I*2)
# p=[''.join(m).strip()[-2::-1]for m in zip(*g(x,I))][1::4]
# q=p[:]
# def f(d,o):
#  for l in g(y.strip(),I):a,b,c=map(int,g(l)[1::2]);d[c-1]+=d[b-1][-a:][::o];d[b-1]=d[b-1][:-a]
#  print(''.join(s[-1]for s in d))
# f(p,-1)
# f(q,1)

# 259
# g=str.split
# x,y=g(open(0).read(),'\n\n')
# p=[''.join(m).strip()[-2::-1]for m in zip(*g(x,'\n'))][1::4]
# def f(d,o):
#  for l in y.splitlines():a,b,c=map(int,g(l)[1::2]);d[c-1]+=d[b-1][-a:][::o];d[b-1]=d[b-1][:-a]
#  print(''.join(s[-1]for s in d))
# f(p[:],-1)
# f(p,1)

# 257 by Starwort#6129
g=str.split
I='\n'
x,y=g(open(0).read()[:-1],2*I)
p=[''.join(m).strip()[-2::-1]for m in zip(*g(x,I))][1::4]
def f(d,o):
 for l in g(y,I):a,b,c=map(int,g(l)[1::2]);d[c-1]+=d[b-1][-a:][::o];d[b-1]=d[b-1][:-a]
 print(''.join(s[-1]for s in d))
f(p[:],-1)
f(p,1)