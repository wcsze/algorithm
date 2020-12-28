import timeit
import random
def find_largest_possible_sum(dp,median,n):
    for j in range(median,-1,-1):
        if(dp[n-1][j]):
            return j

def fair_divide_dp(arr):
    total=0
    n=len(arr)
    for i in range(n):
        total+=arr[i]
    median=total//2
    dp=[[False for i in range(median+1)]for j in range(n)]
    for i in range(n):
        dp[i][0]=True
    for i in range(n):
        for j in range(median+1):
            if(dp[i-1][j]==True):
                dp[i][j]=True
            else:
                dp[i][j]=dp[i-1][j-arr[i]]
    a1=[]
    col=find_largest_possible_sum(dp,median,n)
    while(col>0):
        row=0
        while(dp[row][col]!=True):
            row+=1
        a1.append(arr[row])
        col=col-arr[row]
    
    for i in range(len(a1)):
        arr.remove(a1[i])
    return a1,arr
S=[1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
start=timeit.default_timer()
a1,a2=fair_divide_dp(S)
end=timeit.default_timer()

l1=sum(a1)
l2=sum(a2)
print("Output:")
print("Sum1:",l1)
print("Subset1:",a1)
print("Sum2:",l2)
print("Subset2:",a2)
print(end-start)


