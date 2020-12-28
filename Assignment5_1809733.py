def kth_smallest_fraction(A,k):
    n=len(A)
    low=0
    high=1
    while(low<high):
        j=0
        arr=[0,1]
        mid=(low+high)/2
        L=0
        for i in range(n):
            while(j<n and A[i]/A[j]>mid):
                j+=1
            if(j<n and arr[0]/arr[1]<A[i]/A[j]):
                arr[0]=A[i]
                arr[1]=A[j]
            L+=n-j
        if(L==k):
            return arr
        elif(L>k):
            high=mid
        else:
            low=mid
            
A=[1,2,3,5]
k=3
print(kth_smallest_fraction(A,k))         