from sympy import false


class Solution:
    def hasPathSum(self, root, targetSum):
        """
        :type root: TreeNode
        :type targetSum: int
        :rtype: bool
        """
        def pathfinder(node, sum):
            if not node:
                return False
            sum += node.val
            if node.left == None and node.right == None:
                if sum == targetSum:
                    return True
                sum -= node.val
                return False
            if pathfinder(node.left, sum):
                return True
            if pathfinder(node.right, sum):
                return True
            sum -= node.val

        sum = 0
        return pathfinder(root, sum)
    
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


    # Create a binary tree
    #       5
    #      / \
    #     4   8
    #    /   / \
    #   11  13  4
    #  /  \      \
    # 7    2      1
root = TreeNode(5)
root.left = TreeNode(4)
root.right = TreeNode(8)
root.left.left = TreeNode(20)
root.left.left.left = TreeNode(7)
root.left.left.right = TreeNode(2)
root.right.left = TreeNode(13)
root.right.right = TreeNode(4)
root.right.right.right = TreeNode(1)

s = Solution()
s.hasPathSum(root,20)