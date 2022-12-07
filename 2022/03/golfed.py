# 156
*z,=open(0,'rb')
print(sum((({*a[(l:=len(a)//2):]}&{*a[:l]}).pop()-96)%58for a in z),sum((({*b[:-1]}&{*c}&{*d}).pop()-96)%58for b,c,d in zip(*3*[iter(z)])))

# 148 by Crowthebird#2090
*z,=open(0,'rb')
u=sum
print(u((u({*a[(l:=len(a)//2):]}&{*a[:l]})-96)%58for a in z),u((u({*b[:-1]}&{*c}&{*d})-96)%58for b,c,d in zip(*3*[iter(z)])))
