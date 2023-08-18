s = "bgvyzdsv"

# from hashlib import*
# print(*[next(x for x in map(str,range(9999999))if md5((s+x).encode()).hexdigest()[:i]=="0"*i)for i in[5,6]])

# from hashlib import*
# print(*[next(x for x in map(str,range(9**9))if md5((s+x).encode()).hexdigest()[:i]=="0"*i)for i in[5,6]])

# from hashlib import*
# *map(print([x for x in map(int,range(6**9)][0]if md5((s+x).encode()).hexdigest()[:i]=="0"*i))

# from hashlib import*
# print(*[[x for x in map(str,range(6**9))if"0"*i==md5((s+x).encode()).hexdigest()[:i]][0]for i in[5,6]])


# from hashlib import*
# [print(next(x for x in range(6**9)if"0"*i==md5((s+str(x)).encode()).hexdigest()[:i]))for i in[5,6]]

# from hashlib import*
# [print([x for x in range(6**9)if"0"*i==md5((s+str(x)).encode()).hexdigest()[:i]][0])for i in[5,6]]

from hashlib import*
[print([x for x in range(6**9)if"0"*i==md5(f"{s}{x}".encode()).hexdigest()[:i]][0])for i in[5,6]]

# from hashlib import*
# while 1:md5((s+str(x:=x+1)).encode()).hexdigest()

# from hashlib import*
# print(*[next(filter(lambda x:md5((s+str(x)).encode()).hexdigest()[:i]=="0"*i,range(int(1e9))))for i in[5,6]])
