from functools import reduce


for i, value in enumerate(['A','B','C']):
     print(i,value)


[x*x for x in range(1,11) if x%2==0]


L1=['adam','LISA','barT']

def normalize(name):
     return name.capitalize()

L2=list(map(normalize,L1))
print(L2)
