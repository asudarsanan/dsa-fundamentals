class Node:
    def __init__(self,value) -> None:
        self.value = value
        self.previous = None 

class Stack:
    def __init__(self) -> None:
        self.top = None
    
    def push(self,value):
        newNode = Node(value=value)
        if not self.top:
            self.top = newNode
            return
        else:
            newNode.previous = self.top
            self.top = newNode
            return
    def pop(self):
        if not self.top:
            return None
        current = self.top 
        self.top = current.previous
        current.previous = None
        return current.value
            
    def peek(self):
        if not self.top:
            return None
        else:
            return self.top.value
    
    def size(self):
        if not self.top:
            return None
        count = 1
        current = self.top
        while current.previous != None:
            count +=1
            current = current.previous
        
        return count
        

ss = Stack()
ss.push(1)
print(ss.peek())
ss.push(2)
for i in range (0,10000):
    ss.push(i)

print(ss.peek())

# print(ss.pop())
print(ss.peek())

ss.push(2)
print(ss.size())
print(ss.peek())