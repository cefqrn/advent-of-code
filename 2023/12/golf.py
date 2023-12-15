# from functools import*
# @cache
# def C(l,r):
#  if not r:return'#'not in l
#  c=r[0];return sum(C(l[i+c+1:],r[1:])for i in range(len(l)-c+1)if not('#'in l[:i]or'#'==l[i+c:i+c+1]or'.'in l[i:i+c]))
# *i,=open(0)
# for n in 1, 5:
#  s=0
#  for l in i:l,r=l.split();s+=C("?".join([l]*n),eval(r)*n)
#  print(s)

# from functools import*
# @cache
# def C(l,r):
#  if r:c=r[0];return sum(C(l[i+c+1:],r[1:])for i in range(len(l)-c+1)if not('#'in l[:i]or'#'==l[i+c:i+c+1]or'.'in l[i:i+c]))
#  return'#'not in l
# *i,=open(0)
# for n in 1, 5:
#  s=0
#  for l in i:l,r=l.split();s+=C("?".join([l]*n),eval(r)*n)
#  print(s)

# from functools import*
# C=cache(lambda l,r:r and(c:=r[0])and~sum(~C(l[i+c+1:],r[1:])for i in range(len(l)-c+1)if not('#'in l[:i]or'#'==l[i+c:i+c+1]or'.'in l[i:i+c]))or~('#'not in l))
# *i,=open(0)
# for n in 1,5:
#  s=0
#  for l in i:l,r=l.split();s+=~C("?".join([l]*n),eval(r)*n)
#  print(s)

# C=cache(lambda l,r:r and(c:=r[0])and~sum(~C(l[i-~c:],r[1:])for i in range(len(l)-c+1)if not('#'in l[:i]or'#'==l[i+c:i-~c]or'.'in l[i:i+c]))or~('#'not in l))
# C=cache(lambda l,r:r and(c:=r[0])and~sum(~C(l[i-~c:],r[1:])for i in range(len(l)-c+1)if l[i+c:i-~c]!='#'not in l[:i]and'.'not in l[i:i+c])or~('#'not in l))
# C=cache(lambda l,r:r and(c:=r[0])and~sum(~C(l[i-~c:],r[1:])for i in range(len(l)-c+1)if {'#'}-{l[i+c:i-~c],*l[:i]}and'.'not in l[i:i+c])or~('#'not in l))

from functools import*
C=cache(lambda l,r:r and(c:=r[0])and~sum(~C(l[i-~c:],r[1:])for i in range(len(l)-c+1)if{'#'}-{l[i+c:i-~c],*l[:i]}and{'.'}-{*l[i:i+c]})or~('#'not in l))
*i,=open(0)
for n in 1,5:print(sum(~C("?".join([l]*n),eval(r)*n)for l,r in map(str.split,i)))