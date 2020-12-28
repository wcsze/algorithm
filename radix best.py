import random
def best(n):
    arr=[]
    for i in range(n):
        arr.append(random.randint(0,9))
    return arr
print(best(12))

