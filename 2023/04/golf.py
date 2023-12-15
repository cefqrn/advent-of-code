# c=[1]*194
# p=i=0
# for l in open(0):
#  l=l.split();i+=1;w=len({*l[:12]}&{*l[13:]});p+=2**w//2
#  while w:c[i+w]+=c[i];w-=1
# print(p,sum(c))


# c=[1]*194
# p=q=0
# for l in open(0):l=l.split();w=len({*l[:12]}&{*l[13:]});p+=2**w//2;z,*c=c;q+=z;exec("w-=1;c[w]+=z;"*w)
# print(p,q)


c=[1]*194
p=q=0
for l in open(0):
 l=l.split();z,*c=c;q+=z;i=0
 for _ in{*l[:12]}&{*l[13:]}:c[i]+=z;i+=1
 p+=2**i//2
print(p,q)