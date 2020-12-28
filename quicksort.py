def exchangesort(arr):
    for i in range(len(arr)-1):
        for j in range(i+1,len(arr)):
            if(arr[i]>arr[j]):
                temp=arr[i]
                arr[i]=arr[j]
                arr[j]=temp

arr=[5,3,4,8,2,7,6]
exchangesort(arr)
print(arr)