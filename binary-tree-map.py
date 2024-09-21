from threading import currentThread
from typing import List

from torch import cumulative_trapezoid


class TreeNode:
    def __init__(self,key,val) -> None:
        self.key = key
        self.val = val
        self.left = None
        self.right = None

class TreeMap:
    
    def __init__(self):
        self.root = None

    def insert(self, key: int, val: int) -> None:
        """
        add a new treenode with the key and val atrb.
            if there is no node current -> add the new node as root
            else: find a place where we can add the new node, by comparing the key values and transverse accoding with the current node key
        """
        new_node = TreeNode(key,val)
        if not self.root:
            self.root = new_node
        else:
            current = self.root
            while True: # we are walking the height of the tree, if its balanced, it might reauire to walk o(n)
                if key < current.key:
                    if not current.left:
                        current.left = new_node
                        return
                    current = current.left
                elif key > current.key:
                    if not current.right:
                        current.right = new_node
                        return
                    current = current.right
                else:
                    current.val = val
                    return

    def get(self, key: int) -> int:
        """
        we will walk the tree, looking for the branch where key can be found, 
        if found return the value for the key
            return -1
        """
        if self.root:
            current = self.root
            while current != None:
                if key < current.key:
                    current = current.left
                elif key>current.key:
                    current = current.right
                else:
                    return current.val
            return -1

    def getMin(self) -> int:
        if self.root:
            current = self.root 
            while current.left:
                current = current.left
            return current.val
        return -1
    # Returns the node with the minimum key in the subtree
    def findMin(self, node: TreeNode) -> TreeNode:
        while node and node.left:
            node = node.left
        return node 

    def getMax(self) -> int:
        if self.root:
            current = self.root 
            while current.right:
                current = current.right
            return current.val
        return -1
        
    def remove(self, key: int) -> None:
        self.root = self.removeHelper(self.root, key)

    # Returns the new root of the subtree after removing the key
    def removeHelper(self, curr: TreeNode, key: int) -> TreeNode:
        if curr == None:
            return None

        if key > curr.key:
            curr.right = self.removeHelper(curr.right, key)
        elif key < curr.key:
            curr.left = self.removeHelper(curr.left, key)
        else:
            if curr.left == None:
                # Replace curr with right child
                return curr.right
            elif curr.right == None:
                # Replace curr with left child
                return curr.left
            else:
                # Swap curr with inorder successor
                minNode = self.findMin(curr.right)
                curr.key = minNode.key
                curr.val = minNode.val
                curr.right = self.removeHelper(curr.right, minNode.key)
        return curr

    def getInorderKeys(self) -> List[int]:
        results = []
        self.inorderTriversal(self.root,results)
        return results
    def inorderTriversal(self,root,results):
        if root != None:
            root.left = self.inorderTriversal(root.left,results)
            results.append(root.key)
            root.right = self.inorderTriversal(root.right,results)

td = TreeMap()
td.insert(3,5)
td.insert(1,6)
td.insert(4,7)
td.insert(2,7)
print(td.get(6))
print(td.get(1))
print(td.getMin())
print(td.getInorderKeys())
td.remove(3)
print(td.getInorderKeys())