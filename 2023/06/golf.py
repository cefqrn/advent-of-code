# *l,=open(0)
# for s in'n ':
#     o=1
#     [o:=o*int(((z:=(t*t-4*d)**.5)+t)//2+(z-t)//2+1)
#      for t,d in zip(*(map(int,x[9:].replace(s,'').split())for x in l))]
#     print(o)

# *l,=open(0)
# for s in'n ':
#     o=1
#     [o:=o*sum(d<h*(t-h)for h in range(t))
#      for t,d in zip(*(map(int,x[9:].replace(s,'').split())for x in l))]
#     print(o)

# *l,=open(0)
# for s in ',_':
#     # for t,d in zip(*(map(int,x[9:].replace(s,'').split())for x in l)):
#     for t,d in zip(*(eval(s.join(x[9:].split())+',')for x in l)):
#         print(t, d)


# *p,=open(0)
# for i in',_':e=1;[e:=e*int(((p*p-4*l)**.5+p)//2*2-p+1)for p,l in zip(*(eval(i.join(e[9:].split())+',')for e in p))];print(e)

# for i in',_':e=1;[e:=e*int(((p*p-4*l)**.5+p)//2*2-p+1)for p,l in zip(*(eval(i.join(e[9:].split())+',')for e in open(0)))];print(e)
for i in',_':e=1;[e:=e*int(((p*p-4*l)**.5+p)//2*2-p+1)for p,l in zip(*(eval(i.join(e[9:].split())+',')for e in open(0)))];print(e)

# *p,=open(0)
# for i in'n ':e=1;[e:=e*int((a:=((p*p-4*l)**.5+p)//2)+a-p+1)for p,l in zip(*(map(int,e[9:].replace(i,'').split())for e in p))];print(e)



#  for t,d in zip(*(map(int,x[9:].replace(s,'').split())for x in l)):o*=int(((t*t-4*d)**.5+t)//2+(((t*t-4*d)**.5-t)//2)+1)