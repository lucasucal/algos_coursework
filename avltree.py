class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    if not node:
        return 0
    return node.height

def AVLBalance(node):
    if not node:
        return 0
    return height(node.left) - height(node.right)

def AVLRotateRight(n):
    m = n.left
    l = m.right
    m.right = n
    n.left = l

    m.height = 1 + max(height(m.left), height(m.right))
    n.height = 1 + max(height(n.left), height(n.right))

    return m

def AVLRotateLeft(n):
    m = n.right
    l = m.left
    m.left = n
    n.right = l

    m.height = 1 + max(height(m.left), height(m.right))
    n.height = 1 + max(height(n.left), height(n.right))

    return m

def AVLInsertHelper(self, node, value):
        if not node:
            self.inserted = True
            return Node(value)
        
        if value < node.value:
            node.left = AVLInsertHelper(self, node.left, value)
        elif value > node.value:
            node.right = AVLInsertHelper(self, node.right, value)
        else: 
            return node

        node.height = 1 + max(height(node.left), height(node.right))

        b = AVLBalance(node)
        
        if(b < -1): #right-heavy
            if(value <= node.right.value):
                node.right = AVLRotateRight(node.right)
            return AVLRotateLeft(node)
        elif(b> 1): #left-heavy
            if(value >= node.left.value):
                node.left = AVLRotateLeft(node.left)
            return AVLRotateRight(node)
        
        return node

def searchHelper(node, value):
    while node is not None:
        if value < node.value:
            node = node.left
        elif value > node.value:
            node = node.right
        else:
            return True
    return False

class AVLTree:
    def __init__(self):
        self.root = None
        self.inserted = False


    def insertElement(self, value):
        self.inserted = False
        self.root = AVLInsertHelper(self, self.root, value)
        return self.inserted
    
    def searchValue(self, value):
        return searchHelper(self.root, value)


