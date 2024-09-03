import math
# a = []

# print (a.__len__())


def linearSearch (arr,searchTerm):
    for i in range (0,arr.__len__()):
        print(arr[i],"==>",i)
        if arr[i] == searchTerm:
            return True
        

    return False
    
def twocrystalballs(arr):
    n = len(arr)
    jumpAmt = math.floor(math.sqrt(n))
    print ("jump amt ==>",jumpAmt)

    i=jumpAmt
    while i < n:
        print("before break ==>",i)
        print ("l1 ==> ", arr[i], "i==>",i)
        if arr[i]:
            
            break
        i+=jumpAmt
        print("before break ==>",i)
    
    i-=jumpAmt
    print ("after break ==> ",i)
    j=0
    while j <= jumpAmt and i < n :
        print ("l2 ==> ", arr[i], "i==>",i)
        if arr[i]:
            
            return i
        j+=1
        i+=1
    
    return -1


arr = [False, False,False,False,False,True]
print(twocrystalballs(arr))