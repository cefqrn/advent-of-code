k=50
a=b=0
for l in open(0):exec("k+=1|-(l>'M');b+=k%100<1;"*int(l[1:]));a+=k%100<1
print(a,b)