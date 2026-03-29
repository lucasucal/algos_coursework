from abc import ABC, abstractmethod


# =============================================================================
# Abstract Interface (mirrors the DO NOT MODIFY cell in the notebook)
# =============================================================================

class AbstractSearchInterface(ABC):
    """Abstract class to support search/insert operations."""

    @abstractmethod
    def insertElement(self, element):
        """
        Insert an element in the search tree.
            Parameters:
                element: string to be inserted (str)
            Returns:
                True after successful insertion, False if element already present (bool)
        """
        pass

    @abstractmethod
    def searchElement(self, element):
        """
        Search for an element in the search tree.
            Parameters:
                element: string to be searched (str)
            Returns:
                True if element is found, False otherwise (bool)
        """
        pass


# =============================================================================
# Auxiliary data structure and helper code
# (mirrors the auxiliary cell in the notebook)
# =============================================================================

RED = True
BLACK = False


class LLRBNode:
    """A single node in the LLRB BST, carrying a key, a value, and a link colour."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.color = RED  # new nodes are always inserted as red


def _is_red(node):
    """Return True if node's incoming link is red; None links are black."""
    if node is None:
        return False
    return node.color == RED


def _rotate_left(h):
    """
    Rotate h left to eliminate a right-leaning red link.

    Before:  h ─red─> x        After:  x
                      / \\             / \\
                     b   c         red h   c
                                   / \\
                                  a   b

    Operations:
      1. x (h.right) becomes the new subtree root.
      2. x's left subtree is transferred to h as its new right child.
      3. h becomes x's left child.
      4. x inherits h's original colour (subtree colour unchanged externally).
      5. h is coloured RED (link from x down to h is now red).

    Returns the new subtree root x.
    """
    x = h.right
    h.right = x.left
    x.left = h
    x.color = h.color
    h.color = RED
    return x


def _rotate_right(h):
    """
    Rotate h right to eliminate two consecutive left-leaning red links.

    Before:     h              After:  x
               / \\                   / \\
           red x   c               a   red h
           / \\                         / \\
          a   b                        b   c

    Operations:
      1. x (h.left) becomes the new subtree root.
      2. x's right subtree is transferred to h as its new left child.
      3. h becomes x's right child.
      4. x inherits h's original colour (subtree colour unchanged externally).
      5. h is coloured RED (link from x down to h is now red).

    Returns the new subtree root x.
    """
    x = h.left
    h.left = x.right
    x.right = h
    x.color = h.color
    h.color = RED
    return x


def _flip_colors(h):
    """
    Flip colours of h and both children to split a temporary 4-node.

    Operations:
      1. h is coloured RED  — propagates the carry up to h's parent.
      2. h.left  is coloured BLACK.
      3. h.right is coloured BLACK.

    Modifies nodes in place; returns nothing.
    """
    h.color = RED
    h.left.color = BLACK
    h.right.color = BLACK


def _llrb_put(h, key, value):
    """
    Recursive insert into the subtree rooted at h.

    Going DOWN:
      - h is None          → create and return a new red LLRBNode.
      - key < h.key        → recurse left.
      - key > h.key        → recurse right.
      - key == h.key       → update value in place (no structural change).

    Coming BACK UP (three fix-up checks in order):
      1. Right child red, left child not red  → rotate_left  (no right-leaning reds).
      2. Left child red and left-left red     → rotate_right (no two consecutive reds).
      3. Both children red                   → flip_colors  (split 4-node).

    Returns the (possibly new) subtree root after fix-ups.
    """
    if h is None:
        return LLRBNode(key, value)

    if key < h.key:
        h.left = _llrb_put(h.left, key, value)
    elif key > h.key:
        h.right = _llrb_put(h.right, key, value)
    else:
        h.value = value  # duplicate key: update value

    if _is_red(h.right) and not _is_red(h.left):
        h = _rotate_left(h)
    if _is_red(h.left) and _is_red(h.left.left):
        h = _rotate_right(h)
    if _is_red(h.left) and _is_red(h.right):
        _flip_colors(h)

    return h


def _llrb_contains(root, key):
    """
    Iterative BST search (colour is irrelevant for lookup).

    Traversal:
      - key < node.key → go left.
      - key > node.key → go right.
      - key == node.key → found; return True.
      - node is None   → exhausted; return False.

    Returns True if key exists in the tree, False otherwise.
    """
    node = root
    while node is not None:
        if key < node.key:
            node = node.left
        elif key > node.key:
            node = node.right
        else:
            return True
    return False


# =============================================================================
# LLRB BST API
# (mirrors the LLRB implementation cell in the notebook)
# =============================================================================

class LLRBBST(AbstractSearchInterface):
    """Left-Leaning Red-Black BST implementing AbstractSearchInterface."""

    def __init__(self):
        self.root = None

    def insertElement(self, element):
        """
        Insert element into the tree.

        Operations:
          1. Check for duplicate via _llrb_contains — leave inserted=False if found.
          2. Otherwise delegate to _llrb_put to insert and restore LLRB invariants.
          3. Force root to BLACK (root link is always black).

        Returns True on successful insertion, False if element was already present.
        """
        inserted = False
        if not _llrb_contains(self.root, element):
            self.root = _llrb_put(self.root, element, None)
            self.root.color = BLACK
            inserted = True
        return inserted

    def searchElement(self, element):
        """
        Search for element in the tree.

        Operations:
          Delegates to _llrb_contains for a standard iterative BST traversal.

        Returns True if element is found, False otherwise.
        """
        found = False
        found = _llrb_contains(self.root, element)
        return found
