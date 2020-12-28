
def condition(arr,key,i):
     if(arr[i]==0 and (i+key+1)<len(arr) and arr[i+key+1]==0): 
         return True

def fill_arr(arr,key):
    if(key==0):
        for i in range(len(arr)):
            print(arr[i], end=" ")
        print("")
        return True
    for i in range(len(arr)):
        if(condition(arr,key,i)==True):
            arr[i]=key
            arr[i+key+1]=key
            fill_arr(arr,key-1,)
            arr[i]=0
            arr[i+key+1]=0


        
def twice_distance(n):
    arr=[0]*(2*n)
    fill_arr(arr,n)


n=int(input("enter N:"))
print("Input:N=",n)
print("Output")
twice_distance(n)

