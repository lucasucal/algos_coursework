RED = True
BLACK = False


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.color = RED  # new nodes are always red


class LLRBBST:
    def __init__(self):
        self.root = None

    # --- helper predicates ---

    def _is_red(self, node):
        """
        Checks whether a given node's link is red.
        Returns False for None nodes (null links are treated as black).
        Returns True if node.color == RED, False otherwise.
        """
        if node is None:
            return False
        return node.color == RED

    # --- rotations and colour flip ---

    def _rotate_left(self, h):
        """
        Rotates node h left to fix a right-leaning red link.

        Before:          After:
            h               x
           / \red           / \
          a   x     -->  red h   c
             / \          / \
            b   c        a   b

        Operations:
          1. x becomes the new root of this subtree (was h.right)
          2. x's left subtree is handed off to h as its new right child
          3. h becomes x's left child
          4. x inherits h's original colour so the subtree colour is unchanged
          5. h is coloured RED (the link from x down to h is now red)

        Returns the new subtree root x.
        """
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x

    def _rotate_right(self, h):
        """
        Rotates node h right to fix two consecutive left-leaning red links.

        Before:          After:
              h               x
             / \            /   \
           red x   c  --> a     red h
           / \                   / \
          a   b                 b   c

        Operations:
          1. x becomes the new root of this subtree (was h.left)
          2. x's right subtree is handed off to h as its new left child
          3. h becomes x's right child
          4. x inherits h's original colour so the subtree colour is unchanged
          5. h is coloured RED (the link from x down to h is now red)

        Returns the new subtree root x.
        """
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RED
        return x

    def _flip_colors(self, h):
        """
        Flips the colours of node h and both its children.
        Used when both children are red (a temporary 4-node that must be split).

        Operations:
          1. h is coloured RED  — passes the "carry" upward to h's parent
          2. h.left  is coloured BLACK
          3. h.right is coloured BLACK

        Returns nothing; modifies nodes in place.
        """
        h.color = RED
        h.left.color = BLACK
        h.right.color = BLACK

    # --- put ---

    def put(self, key, value=None):
        """
        Public insert/update method.

        Operations:
          1. Delegates to the recursive _put helper to find the correct position
             and perform any necessary fix-ups on the way back up.
          2. Forces the root to BLACK after every insertion (LLRB invariant:
             the root link is always black).

        Returns nothing.
        """
        self.root = self._put(self.root, key, value)
        self.root.color = BLACK

    def _put(self, h, key, value):
        """
        Recursive helper that inserts (key, value) into the subtree rooted at h
        and restores the three LLRB invariants on the way back up.

        Operations — going DOWN the tree:
          1. Base case: h is None  → create and return a new red Node.
          2. key < h.key           → recurse into the left subtree.
          3. key > h.key           → recurse into the right subtree.
          4. key == h.key          → key already exists; update its value in place.

        Fix-up on the way BACK UP (three cases checked in order):
          1. Right child is red AND left child is not red
               → rotate_left(h)  — eliminates a right-leaning red link.
          2. Left child is red AND left-left grandchild is also red
               → rotate_right(h) — eliminates two consecutive red links on the left.
          3. Both children are red
               → flip_colors(h)  — splits the 4-node and pushes the carry upward.

        Returns the (possibly new) root of this subtree after fix-ups.
        """
        if h is None:
            return Node(key, value)

        if key < h.key:
            h.left = self._put(h.left, key, value)
        elif key > h.key:
            h.right = self._put(h.right, key, value)
        else:
            h.value = value  # update value for existing key

        # fix-up: maintain LLRB invariants on the way back up
        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)

        return h

    # --- get ---

    def get(self, key):
        """
        Searches for key in the tree using standard BST traversal
        (colour is irrelevant for search).

        Operations — iterative, starting from the root:
          1. key < node.key → move to the left child.
          2. key > node.key → move to the right child.
          3. key == node.key → key found; stop.
          4. node is None    → key not present; stop.

        Returns the value associated with key if found, or None if the key
        does not exist in the tree.
        """
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None
