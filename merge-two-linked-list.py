# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val < list2.val:
             list1.next = mergeTwoLists(list1.next, list2)
             return list1
        else:
             list2.next = mergeTwoLists(list1,list2.next)
             return list2
             

# Create the first linked list: 1 -> 2 -> 4
l1 = ListNode(1)
l1.next = ListNode(2)
l1.next.next = ListNode(4)

# Create the second linked list: 1 -> 3 -> 5
l2 = ListNode(1)
l2.next = ListNode(3)
l2.next.next = ListNode(5)

# Merge the two lists
merged = mergeTwoLists(l1, l2)

# Print the merged list
current = merged
while current:
    print(current.val, end=" -> ")
    current = current.next
print("None")