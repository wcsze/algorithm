
def partition(low,high,arr):
    pivotitem=arr[low]
    j=low
    for i in range(low+1,high+1):
        j+=1
        arr[i],arr[j]=arr[j],arr[i]
    pivot=j
    arr[low],arr[pivot]=arr[pivot],arr[low]

def selection(low,high,arr,k):
    pivot=low
    if(low==high):
        return arr[low]
    else:
        partition(low,high,arr,k)
        if(k==pivot):
            return arr[pivot]
        elif(k<pivot):
            return selection(low,pivot-1,arr,k)
        else:
            return selection(pivot+1,high,arr,k)