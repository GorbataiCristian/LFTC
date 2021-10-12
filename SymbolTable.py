class SymbolTableNode:
    def __init__(self, key, id):
        self.key = key
        self.id = id
        self.left = None
        self.right = None
        self.parent = None

    # inserts a new node based on its value
    def insert_elem(self, node):
        if node.key == self.key:
            return True
        if node.key < self.key:
            if self.left is None:
                self.left = node
                node.parent = self
                return False
            else:
                self.left.insert_elem(node)
        elif node.key > self.key:
            if self.right is None:
                self.right = node
                node.parent = self
                return False
            else:
                self.right.insert_elem(node)

    def delete_elem(self, key):
        if key < self.key:
            if self.left:
                return self.left.delete_elem(key)
            else:
                print('not found')
                return False, None
        elif key > self.key:
            if self.right:
                return self.right.delete_elem(key)
            else:
                print('not fount')
                return False, None

        elif key == self.key:
            if self.left is None and self.right is None:
                if not self.parent:
                    return True, None
                self.parent.replace_child(self, None)
                return False, None
            elif self.left is None:
                if not self.parent:
                    return True, self.right
                self.parent.replace_child(self, self.right)
                return False, None
            elif self.right is None:
                if not self.parent:
                    return True, self.left
                self.parent.replace_child(self, self.left)
                return False, None
            else:
                min_of_right = self.right
                while min_of_right.left:
                    min_of_right = min_of_right.left
                min_of_right.parent.replace_child(min_of_right, None)
                min_of_right.left = self.left
                min_of_right.right = self.right
                if not self.parent:
                    return True, min_of_right
                self.parent.replace_child(self, min_of_right)
                return False, None

    def replace_child(self, old_child, new_child):
        if self.left and self.left.key == old_child.key:
            self.left = new_child
        elif self.right and self.right.key == old_child.key:
            self.right = new_child
        else:
            print('error in SymbolTableNode::replace_child')

    def inorder_traversal(self):
        if self.left is not None:
            self.left.inorder_traversal()
        print(self.key, self.id, end='; ')
        if self.right is not None:
            self.right.inorder_traversal()
# SymbolTable implemented as a binary search tree
# each node is a SymbolTableNode
class SymbolTable:
    def __init__(self):
        self.root = None
        self.id = 0
    def inorder_traversal(self):
        if self.root is not None:
            self.root.inorder_traversal()

    def add_val(self, key):
        new_node = SymbolTableNode(key, self.id)
        if self.root is None:
            self.root = new_node
        else:
            found = self.root.insert_elem(new_node)
            if not found:
                self.id += 1
    def delete_val(self, key):
        if self.root is None:
            print('not found')
        else:
            was_root_changed, new_root = self.root.delete_elem(key)
            if was_root_changed:
                print(1)
                self.root = new_root


ST = SymbolTable()
ST.add_val('d')
ST.add_val('b')
ST.add_val('a')
ST.add_val('c')
ST.add_val('min')
ST.add_val('max')
ST.delete_val('d')
ST.inorder_traversal()