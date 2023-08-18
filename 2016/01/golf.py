# s={0}
# c=p=0
# q=None
# f=lambda x:int(abs(x.real)+abs(x.imag))
# for d in input().split(', '):c+=d<'R'or-1;exec("p+=1j**(c%4);q=[q,p][q is None and p in s];s|={p};"*int(d[1:]))
# print(f(p),f(q))

p=q=0
c,*s=1,
for d in input().split(", "):c*=1j**-~ord(d[0]);exec("p+=c;q=q or(p in s)*p;s+=p,;"*int(d[1:]))
f=lambda x:int(abs(x.real)+abs(x.imag))
print(f(p),f(q))