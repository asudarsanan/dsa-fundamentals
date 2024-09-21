def inorderTraversal(self, root):
    """
    :type root: TreeNode
    :rtype: List[int]
    """
    result = []
    def inorder(root):
        if not root:
            return 
        inorder(root.left)
        result.append(root.val)
        inorder(root.right)
    inorder(root)
    return result


