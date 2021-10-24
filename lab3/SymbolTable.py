import numpy as np

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
            return self.id
        if node.key < self.key:
            if self.left is None:
                self.left = node
                node.parent = self
                return node.id
            else:
                return self.left.insert_elem(node)
        elif node.key > self.key:
            if self.right is None:
                self.right = node
                node.parent = self
                return node.id
            else:
                return self.right.insert_elem(node)

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
        l = r = None
        if self.left is not None:
            l = self.left.inorder_traversal()
        if self.right is not None:
            r = self.right.inorder_traversal()
        return ([l] if not l else l) + [str(self.key) + '->' + str(self.id)] + ([r] if not r else r)


# SymbolTable implemented as a binary search tree
# each node is a SymbolTableNode
class SymbolTable:
    def __init__(self):
        self.root = None
        self.id = 0
    def inorder_traversal(self):
        if self.root is not None:
            return [e for e in self.root.inorder_traversal() if e]

    def add(self, key):
        new_node = SymbolTableNode(key, self.id)
        if self.root is None:
            self.root = new_node
            self.id = 1
            return 0
        else:
            id = self.root.insert_elem(new_node)
            # if node was inserted
            if id == self.id:   
                self.id += 1
            return id
    def delete(self, key):
        if self.root is None:
            print('not found')
        else:
            was_root_changed, new_root = self.root.delete_elem(key)
            if was_root_changed:
                self.root = new_root


ST = SymbolTable()
ST.add('d')
ST.add('b')
ST.add('a')
ST.add('c')
ST.add('min')
ST.add('max')
ST.delete('d')
print(ST.inorder_traversal())
