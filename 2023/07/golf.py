# S=sorted
# B=lambda h,r:max((S(map((n:=h.replace(r,p)).count,{*n}))[::-1],*map(f"{r}23456789TJQKA".find,h))for p in{*h})
# *l,=map(str.split,open(0))
# for r in":J":i=0;print(sum(b*(i:=i+1)for(_,b)in S((B(h,r),int(b))for h,b in l)))


# S=sorted
# *l,=map(str.split,open(0))
# for r in":J":B=lambda h:max((S(map((n:=h.replace(r,p)).count,{*n}))[::-1],*map(f"{r}23456789TJQKA".find,h))for p in{*h});i=0;print(sum(b*(i:=i+1)for(_,b)in S((B(h),int(b))for h,b in l)))

# S=sorted
# *l,=map(str.split,open(0))
# for r in":J":i=0;print(sum(b*(i:=i+1)for(_,b)in S((max((S(map(h.replace(r,p).count,{*h.replace(r,p)}))[::-1],*map(f"{r}23456789TJQKA".find,h))for p in{*h}),int(b))for h,b in l)))

# S=sorted
# *l,=map(str.split,open(0))
# for r in":J":i=0;print(sum(b*(i:=i+1)for(_,b)in S((max((S(map(h.replace(r,p).count,h.replace(r,p)))[::-1],*map((r+"23456789TJQKA").find,h))for p in h),int(b))for h,b in l)))


S=sorted
*l,=open(0)
for r in":J":f=lambda z:S(map(z.count,z))[::-1];i=0;print(sum(int(s[6:])*(i:=i+1)for s in S(l,key=lambda x:max((f(x[:5].replace(r,p)),*map((r+"23456789TJQKA").find,x))for p in x))))
# for r in":J":f=lambda z:S(map(z.count,z))[::-1];i=0;print(sum(b*(i:=i+1)for(_,b)in S((max((f(x[:5].replace(r,p)),*map((r+"23456789TJQKA").find,x))for p in x),int(x[6:]))for x in l)))
# for r in":J":i=0;print(sum(int(s[6:])*(i:=i+1)for s in S(l,key=lambda x:max((S(map(x[:5].replace(r,p).count,x[:5].replace(r,p)))[::-1],*map((r+"23456789TJQKA").find,x))for p in x))))
