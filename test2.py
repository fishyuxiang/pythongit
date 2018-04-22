def add_end(L=None):
    if L is None:
        L=[]
    L.append('END')
    return L
add_end()

def calc(numbers):
    sum=0
    for n in numbers:
        sum=sum+n*n
    return sum
calc([1,2,3])

def calc(*numbers):
    sum=0
    for n in numbers:
        sum=sum+n*n
    return sum

calc(1,2,3)
calc(1,2,3,4,5)
