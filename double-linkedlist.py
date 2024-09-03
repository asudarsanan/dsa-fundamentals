import sys

class Node:
    def __init__(self,value):
        self.value = value
        self.previous = None
        self.next = None

class DoubleLinkedList:
    def __init__(self,head=None):
        self.head = head
    
    def append(self,new_node):
        current = self.head
        if current:
            while current.next:
                current = current.next
            new_node.previous = current
            current.next = new_node
            new_node.next = None
        else:
             self.head = new_node

    def display(self):
        current = self.head
        count = 0
        if current == None:
            print ("No Values")
        else:
            while current:
                print ("pos ==>",count,"value ==> ",current.value)
                current = current.next
                count +=1


    def insert(self,new_node,pos):
        current = self.head
        count = 0
        if pos == 0:
            new_node.next = current
            new_node.previous = current.previous
            current.previous=new_node
            self.head = new_node
            return
        if current is None:
            self.head = new_node
            return
        

        while count < pos and current:
            current = current.next 
            count +=1
        if current:


            new_node.next = current
            new_node.previous = current.previous
            current.previous.next = new_node
            return


            

        


a = Node(1)


b = Node("suda")
c = Node("asuda")
c.previous=None
c.next=None
dll = DoubleLinkedList()
dll.append(a)
dll.append(b)
dll.insert(c,0)
dll.display()
print(sys.getsizeof(dll))