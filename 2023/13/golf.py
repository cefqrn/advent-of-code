def R(b,n):
 o={0}
 for m in 100,1:l=len(b);i=0;exec("i+=1;o|={i*m*(n>sum(c!=d for c,d in zip(''.join(map(''.join,b[:i][::-1])),''.join(map(''.join,b[i:])))))};"*~-l);b=*zip(*b),
 return o
p=q=0
for b in map(str.split,open(0).read().split('\n\n')):p+=sum(z:=R(b,1));q+=sum(R(b,2)-z)
print(p,q)
