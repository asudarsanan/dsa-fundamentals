class Node:
    def __init__(self,val=None,next=None,prev=None):
        self.val = val
        self.next = next
        self.prev = prev
class MyLinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        

    def get(self, index):
        """
        :type index: int
        :rtype: int

        we have to init a counter from 0 and walk until the counter is same as the index
        return the value at the index
        """
        count = 0
        current = self.head 
        if self.head and index == 0: #best case o(1)
            return current.val
        elif self.head == None:
            return -1
        else:
            while count < index and current: #O(n) if the index is the last or out of bound
                if not current.next:
                    return -1 #index outbound
                current = current.next
                count +=1
            return current.val


    def addAtHead(self, val):
        """
        :type val: int
        :rtype: None

        current will be pointing to head, we have to make the current head point back to the new  node and new node point to current and swap 
        the head to new node
        edge cases: no head, the new node will be the head and tail
        """
        new_node = Node(val)
        if not self.head: #setting head as val node is head not present
            self.head = new_node
            self.tail = new_node
            self.length +=1
        else:
            current = self.head
            current.prev = new_node
            new_node.next = current
            self.head = new_node
            self.length +=1

    def addAtTail(self, val):
        """
        :type val: int
        :rtype: None

        we have to point the current tail.next from none to the new node and make the new_node.prev as the current tail
        update the tail back to the new_node
        edge case = tail doesn't exist => make the new_node as tail and head 
        """
        new_node = Node(val)
        if not self.tail:
            self.tail = new_node
            self.head = new_node
            self.length +=1
        else:
            curr = self.tail
            curr.next = new_node
            new_node.prev = curr
            self.tail = new_node
            self.length +=1

    def addAtIndex(self, index, val):
        """
        :type index: int
        :type val: int
        :rtype: None

        we have to count and walk till the index, this would give the current value at index, grab and update the next of (current.prev) as new_node
        make the new_node.next as the current node along with new_node.prev as the current.prev
        edge cases: index doesn't exis ==> if not current.next at some point lets exit the loop?
                    what if index is head or tail ==> call the add at head or add at tail func
        """
        
        
        if index > self.length:
            return 
        elif index == 0:
            self.addAtHead(val)
        elif index == self.length:
            self.addAtTail(val)
        else:
            count =0
            current = self.head
            new_node = Node(val)
            while current and count < index:
                if current.next == None:
                    return
                current = current.next
                count+=1
                
            prev = current.prev
            prev.next = new_node
            new_node.next = current
            current.prev = new_node
            new_node.prev = prev
            self.length +=1



    def deleteAtIndex(self, index):
        """
        :type index: int
        :rtype: None


        we have walk till the index and make the previosu record point to the current.next directly decoupling the current value entirly
        edge cases: head and tail non = empty list retrun none
                    if the index is out bound --> when we walk and notice that the next value is not present we have reched the end of the linked list
                    if the index is still not found then we have to return
        """
        if index < 0 or index >= self.length:
            return
        if index == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif index == self.length - 1:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            prev = current.prev
            next = current.next
            prev.next = next
            next.prev = prev
        self.length -= 1






# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)