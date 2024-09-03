class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self,head=None,rear=None):
        self.head = head
        self.rear = rear

    def peak(self):
        if not self.head:
            raise Exception("Empty Queue Execption")
        if self.head:
            return self.head.value
        
    def enqueue(self,newElement):
        if not self.head:
            self.head = self.rear = newElement
        else:
            self.rear.next = newElement
            self.rear = newElement
            newElement.next = None
    
    def dequeue(self):
        if not self.head:
            raise Exception("Empty Queue Execption")
        else:
            head = self.head
            self.head = head.next
            head.next = None
            return head.value
        
    def size(self):
        if self.head ==None and self.rear == None:
            count =0
        else:
            count = 1
            current = self.head
            while current != self.rear:
                count +=1
                current = current.next
                
        return count



a = Node("A")
b = Node("B")
c = Node("C")

qq = Queue()
qq.enqueue(a)
print(qq.peak())
qq.enqueue(b)
qq.enqueue(c)
print(qq.size())
# print(qq.dequeue())
# print(qq.dequeue())
# print(qq.peak())