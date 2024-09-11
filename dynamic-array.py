"""
pushback = insert at the end, this needs a resize if length is the capacity
resize = create a new arr with double the capacity and copy the contents to exact indecies in the new arr, dealloc the current arr
pop = remove the last element in the array and adjust the length pointer
get = display value based on the index
insert = insert at a position and shift the reest of the value
print/display = iterate and display all the items in the arr.
"""
import re

from networkx import capacity_scaling


class DynamicArray:
    def __init__(self,capacity=None) -> None:
        self.capacity = capacity
        self.length = 0 #incremented based on the insert operation and decremented based on the delete opertation.
        self.arr = [0]*self.capacity #create arr of capacity

    def resize(self):
        new_capacity = self.capacity*2
        new_arr = [0]*new_capacity

        if len(self.arr) > 0:
            for i in range(len(self.arr)):
                new_arr[i] = self.arr[i]
        print(self.arr,"==>",new_arr) #4 debug
        self.capacity = new_capacity
        self.length = self.length
        self.arr = new_arr

    def pushback(self,value):
        if self.length >= self.capacity:
            self.resize()
        self.arr[self.length] = value
        self.length+=1
        return self.arr,self.length
    def popback(self):
        if self.length > 0:
            self.length-=1

    def insert(self,pos,value):
        if pos < self.length:
            self.arr[pos] = value
        else:
            raise Exception("Index out of bound")
        return self.arr
    def get(self,pos):
        if pos < self.length:
            return self.arr[pos]
    def getSize(self):
        return self.length
    def getCapacity(self):
        return self.capacity

da = DynamicArray(2)
# da.resize()
print(da.pushback(23))
print(da.pushback(23))
print(da.pushback(23))
da.popback()
print(da.pushback(24))
print(da.insert(2,25))
print(da.getCapacity(),da.getSize())




