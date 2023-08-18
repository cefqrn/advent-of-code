with open("_") as f:
    s = f.read()

# takes in input (132 chars)
*x,=map(lambda x:sorted(map(int,x.split('x'))),open("_"));print(*map(sum,zip(*[[a*b*3+c*(y:=(a+b)*2),a*b*c+y]for a,b,c in x])))
# *x,=map(lambda x:sorted(map(int,x.split('x'))),open("_"));print(*map(sum,zip(*[[a*b+(a*(b+c)+b*c)*2,a*b*c+(a+b)*2]for a,b,c in x])))

# prints (127 chars)
*x,=map(lambda x:sorted(map(int,x.split('x'))),s.split());print(*map(sum,zip(*[[a*b*3+c*(y:=(a+b)*2),a*b*c+y]for a,b,c in x])))
# *x,=map(lambda x:sorted(map(int,x.split('x'))),s.split());print(*map(sum,zip(*[[a*b*3+c*(a+b)*2,a*b*c+(a+b)*2]for a,b,c in x])))
# *x,=map(lambda x:sorted(map(int,x.split('x'))),s.split());print(*map(sum,zip(*[[a*b+(a*(b+c)+b*c)*2,a*b*c+(a+b)*2]for a,b,c in x])))
*x,=map(lambda x:sorted(map(int,x.split('x'))),s.split());print(*map(sum,zip(*[[2*(a*b+b*c+a*c),a*b*c+(a+b)*2]for a,b,c in x])))

# 136
*x,=map(lambda x:sorted(map(int,x.split('x'))),s.split());print(sum(a*b+(a*(b+c)+b*c)*2for a,b,c in x),sum(a*b*c+(a+b)*2for a,b,c in x))

#evals (135 chars)
(x:=list(map(lambda x:sorted(map(int,x.split('x'))),s.split())))and sum(a*b*3+c*(a+b)*2for a,b,c in x),sum(a*b*c+(a+b)*2for a,b,c in x)
