class Node:
    def __init__(self,value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self,head=None):
        self.head = head
    def append(self,new_node):
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new_node
        
        else:
            self.head = new_node
    def delete(self,value):
        current = self.head
        if current.value == value:
            self.head = current.next
        else:
            while current:
                if current.value == value:
                    break
                prev = current
                current = current.next
            if current == None:
                return 
            prev.next = current.next
            current = None
    def display(self):
        count = 0
        current = self.head
        while current:
            print("pos==>",count,"value ==>",current.value)
            current = current.next
            count +=1    
    def insert(self,new_node,position):
         count=0
         current = self.head
         if current == None:
             self.head = new_node
             return
         elif position == 0 :
             self.head = new_node
             new_node.next = current
         else:
            
            while count < position and current:
                prev = current
                current = current.next     
                count+=1
            new_node.next = current
            prev.next = new_node
            
    

a = Node(1)
b = Node(2)
c = Node ("asuda")
d = Node("vasuda")

number = LinkedList(a)
number.append(b)
number.append(c)
# print(number)
# number.delete(2)
# print(number)
number.insert(d,5)
number.display()