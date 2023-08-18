with open("day01/input") as f:
    s = f.read()

x=0
[x:=1 for _ in "123"]
{x:=1 for _ in "123"}

# golfed
print((f:=1)+(l:=[f:=f+(1|-(x==')'))for x in s]).index(0),l[-1]-1)

# print(eval(s.replace('(','+1').replace(')','-1')))

# # f = 0
# # p2 = False
# # for i, char in enumerate(s):
# #     f += 1 if char == "(" else -1
    
# #     if f < 0 and not p2:
# #         print(f"reached the basement at pos {i + 1} (p2)")
# #         p2 = True

# # print(f"ended at floor {f} (p1)")


# # golfed p1
# print(sum(1|-(c==')')for c in s))

# # golfed p2
# print((f:=1)+[f:=f+(1|-(x==')'))for x in s].index(0))

# from itertools import accumulate, takewhile, chain
# print(sum(1 for _ in takewhile(lambda x:x>0,accumulate(map(lambda x:1|-(x==')'),'a'+s)))))
