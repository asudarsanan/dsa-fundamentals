from typing import List

from sympy import true


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
class LinkedList:
    
    def __init__(self):
        self.head = None
        self.tail = None

    
    def get(self, index: int) -> int:
        current = self.head.next
        count = 0
        while current and count < index:

            if count == index:
                return current.value
            else:
                current = current.next
                count+=1
        return -1


        

    def insertHead(self, val: int) -> None:
        node = Node(val)
        if self.head == None:
            self.head = node 
            self.tail = node
        else:
            node.next = self.head
            self.head = node

        

    def insertTail(self, val: int) -> None:
        node = Node(val)
        if self.tail == None:
            self.tail = node
            self.head = node
        else:
            self.tail.next = node
            self.tail = node
        

    def remove(self, index: int) -> bool:
        count = 0
        current = self.head
        while count < index and current:
            count+=1
            prev = current
            current = current.next
        if current and current.next:
            if current == self.tail:
                self.tail = prev
            prev.next = current.next
            return True
        return False
        
                
        

    def getValues(self) -> List[int]:
        if self.head == None:
            return
        else:
            vals = []
            current = self.head
            while current:
                vals.append(current.value)
                current = current.next
            return vals
                

        
ll = LinkedList()

ll.insertHead(1)
ll.insertTail(2)
ll.insertHead(0)
ll.remove(1)
ll.getValues()
