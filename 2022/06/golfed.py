# s=input()
# for j in 3,13:print([i for i,_ in enumerate(s)if len({*s[i+~j:i]})>j][0])

# s=input()
# for j in 3,13:print([i for i in range(len(s))if len({*s[i+~j:i]})>j][0])

# s=input()
# for j in 3,13:print([i for i in range(9999)if len({*s[i+~j:i]})>j][0])

# s=input()
# for j in 4,14:print([i for i in range(9999)if len({*s[i-j:i]})+j][0])

for j in 3,13:print([i for i in range(4096)if len({*input()[i+~j:i]})>j][0])