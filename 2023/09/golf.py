p=q=0
for c in open(0):
 *d,=map(int,c.split());s=1
 while any(d):q+=d[-1];p+=d[0]*s;s=-s;*d,=map(int.__sub__,d[1:],d)
print(p,q)
