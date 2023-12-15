# import re
# i=p=q=0
# for l in open(0):i+=1;r,g,b=eval('max(map(int,re.findall("\d+(?= %s)",l)+[0])),'*3%(*"rgb",));p+=i*(r<13>=g<15>b);q+=r*g*b
# print(p,q)

import re
i=p=q=0
for l in open(0):i+=1;exec('%s=max(map(int,re.findall("\d+(?= %s)",l)+[0]));'*3%(*2*"rgb",));p+=i*(b<13>=r<15>g);q+=r*g*b
print(p,q)

# rg
# br
# gb
