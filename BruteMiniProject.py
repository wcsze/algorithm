import timeit
import random
import numpy as np
def fair_divide_bf(S):
    N = len(S)
    total=sum(S)
    minDiff=np.inf
    comb2 = S
    # loop through 2 ** N possible combinations
    for i in range(2 ** N):
        comb1 = []
        for j in range(N):
            if (i >> j) % 2 == 1:
                comb1.append(S[j])
        sumComb2 = total - sum(comb1)
        diffSubset = abs(sumComb2 - sum(comb1))
        if(diffSubset < minDiff):
            minDiff = diffSubset
            minCombo = comb1
        
    for items in minCombo:
        comb2.remove(items)
    return minCombo, comb2
S=[1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
start=timeit.default_timer()
comb1, comb2 =fair_divide_bf(S)
end=timeit.default_timer()



sum1 = sum(comb1)
sum2 = sum(comb2)

print("Output:")
print("Sum1:",sum1)
print("Subset1:",comb1)
print("Sum2:",sum2)
print("Subset2:",comb2)
print(end-start)