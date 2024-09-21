import matplotlib.pyplot as plt

class BSTNode:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

class BSTMap:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value, node)
            else:
                self._insert_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, value, node)
            else:
                self._insert_recursive(node.right, key, value)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def delete(self, key):
        node = self.search(key)
        if node is not None:
            self._delete_recursive(node)

    def _delete_recursive(self, node):
        if node.left is None and node.right is None:
            if node.parent is None:
                self.root = None
            elif node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None
        elif node.left is None:
            if node.parent is None:
                self.root = node.right
            elif node.parent.left == node:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
        elif node.right is None:
            if node.parent is None:
                self.root = node.left
            elif node.parent.left == node:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
        else:
            successor = self.find_successor(node)
            node.key = successor.key
            node.value = successor.value
            self._delete_recursive(successor)

    def find_successor(self, node):
        if node.right is not None:
            return self.find_successor(node.right)
        else:
            while node.parent is not None and node.parent.right == node:
                node = node.parent
            return node.parent

    def create_tree_map(self, colors=None):  # Make colors optional
        """
        Creates a tree map based on the BST.

        Args:
            colors (dict, optional): A dictionary mapping keys to colors. Defaults to None.
                If None, a default color scheme will be used.
        """

        if colors is None:  # Use a default color scheme if not provided
            colors = {key: f"C{i}" for i, key in enumerate(self.in_order_traversal())}


        def draw_rectangles(node, x, y, width, height, color):
            ax.add_patch(plt.Rectangle((x, y), width, height, color=color))
            ax.text(x + width / 2, y + height / 2, f"{node.key}: {node.value}", ha='center', va='center')

        def create_rectangles(node, x, y, width, height, colors):
            if node is None:
                return
            if node.left is not None:
                create_rectangles(node.left, x, y, width / 2, height, colors)
            if node.right is not None:
                create_rectangles(node.right, x + width / 2, y, width / 2, height, colors)
            draw_rectangles(node, x, y, width, height, colors[node.key])

        fig, ax = plt.subplots()
        create_rectangles(self.root, 0, 0, 1, 1, colors)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        plt.show()
# Example usage
bst_map = BSTMap()
bst_map.insert(5, 10)
bst_map.insert(3, 5)
bst_map.insert(7, 15)
bst_map.insert(2, 3)
bst_map.insert(4, 7)
bst_map.insert(6, 12)
bst_map.insert(8, 17)

colors = {key: f"C{i}" for i, key in enumerate(bst_map.search(10).key)}
bst_map.create_tree_map(colors)