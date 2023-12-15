# def h(s,v=0):
#  for c in s:v=17*(v+ord(c))
#  return v%256

# def h(s,v=0):[v:=17*(v+ord(c))for c in s];return v%256
# h=lambda s,v=0:[v:=17*(v+ord(c))for c in s][-1]%256

# b=eval('{},'*256)
# p=q=u=0
# for s in input().split(','):
#  d=s[:s.find('=')];k=0;*_,x,y,_=[k:=17*(k+ord(c))%256for c in s];p+=k
#  if s>d+'-':b[x][d]=s
#  else:b[y].pop(d,0)
# for c in b:
#  u+=1;v=0
#  for i in c:v+=1;q+=u*v*int(c[i][-1])
# print(p,q)

b=eval('{},'*256)
p=q=u=0
for s in input().split(','):d=s[:s.find('=')];k=0;*_,x,y,_=[k:=17*(k+ord(c))%256for c in s];p+=k;s>d+'-'!=exec("b[x][d]=s")or b[y].pop(d,0)
for c in b:
 u+=1;v=0
 for i in c:v+=1;q+=u*v*int(c[i][-1])
print(p,q)


# b=eval('{},'*256)
# p=q=u=0
# for s in input().split(','):
#  d=s[:s.find('=')];k=0;*x,=[k:=17*(k+ord(c))%256for c in s];p+=k
#  if s>d+'-':b[x[-3]][d]=s
#  else:b[x[-2]].pop(d,0)
# for c in b:
#  u+=1;v=0
#  for i in c:v+=1;q+=u*v*int(c[i][-1])
# print(p,q)


# b=eval('{},'*256)
# p=q=u=0
# for s in input().split(','):
#  d=s[:s.find('=')];k=0;*_,x,y,_=[k:=17*(k+ord(c))%256for c in s];p+=k
#  if s>d+'-':b[x][d]=s
#  else:b[y].pop(d,0)
# for c in b:u+=1;v=0;q+=u*sum((v:=v+1)*int(c[i][-1])for i in c)
# print(p,q)


# b=eval('{},'*256)
# p=u=0
# for s in input().split(','):
#  d=s[:s.find('=')];k=0;*_,x,y,_=[k:=17*(k+ord(c))%256for c in s];p+=k
#  if s>d+'-':b[x][d]=s
#  else:b[y].pop(d,0)
# print(p,sum([u:=u+1][v:=0]*sum((v:=v+1)*int(c[i][-1])for i in c)for c in b))


# A=B=n=0;b=eval('{},'*256)
# for y in input().split(','):
#  t=i=0
#  for x in y:x in'-='!=exec("I=i;T=t");t=(t+ord(x))*17%256;i+=1
#  b[T][l:=y[:I]]=int(g:=y[I+1:]or 0);g==0<b[T].pop(l,0);A+=t
# for x in b:
#  n+=1;j=0
#  for z in x:j+=1;B+=n*j*x[z]
# print(A,B)

# for step in i:z,*n=step.split('=');exec("b[h(z)]"+(n and"[z],=n"or".pop(z,0)"))
#  exec("b[h(z)]"+[".pop(z,0)","[z],=n"][n>[]])