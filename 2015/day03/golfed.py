with open("input") as f:
    s = f.read()

# end of setup

# 112 chars
f,l=lambda b,a=0,x=0:{0}|{x:=x+(1|-(c in">v"))*1j**(c in"^v")for c in s[a::b]},len;print(l(f(1)),l(f(2)|f(2,1)))

# alternative using map
f=lambda b,a=0,x=0:{0}|{x:=x+(1|-(c in">v"))*1j**(c in"^v")for c in s[a::b]};print(*map(len,[f(1),f(2)|f(2,1)]))

# 97
f=lambda b,a=0,x=0:{0}|{x:=x+1j**'>^<'.find(c)for c in s[a::b]}
print(len(f(1)),len(f(2)|f(2,1)))

# 97
f=lambda b,a=0,x=0:{0}|{x:=x+1j**'>v<'.find(c)for c in s[a::b]}
print(len(f(1)),len(f(2)|f(2,1)))

# 96
f=lambda a,x=0:{0}|{x:=x+1j**'>v<'.find(c)for c in s[a//4::a&3]}
print(len(f(1)),len(f(2)|f(6)))

# 95
f=lambda a,x=0:{0}|{x:=x+1j**'>v<'.find(c)for c in s[a>3::a&3]}
print(len(f(1)),len(f(2)|f(6)))

print(len((f:=lambda b,a=0,x=0:{0}|{x:=x+1j**'>v<'.find(c)for c in s[a::b]})(1)),len(f(2)|f(2,1)))

# 192 chars
# x=y=z=0;print(l({0}|{(x:=x+(1|-(c in">v"))*1j**(c in"^v"))for c in s}),len({0}|{(y:=y+(1|-(c in">v"))*1j**(c in"^v"))for c in s[0::2]}|{(z:=z+(1|-(c in">v"))*1j**(c in"^v"))for c in s[1::2]}))