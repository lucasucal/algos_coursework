from abc import ABC, abstractmethod


class AbstractSearchInterface(ABC):
    """
    Abstract class to support search/insert operations (plus underlying data structure)

    """

    @abstractmethod
    def insertElement(self, element):
        """
        Insert an element in a search tree
            Parameters:
                    element: string to be inserted in the search tree (string)

            Returns:
                    "True" after successful insertion, "False" if element is already present (bool)
        """

        pass

    @abstractmethod
    def searchElement(self, element):
        """
        Search for an element in a search tree
            Parameters:
                    element: string to be searched in the search tree (string)

            Returns:
                    "True" if element is found, "False" otherwise (bool)
        """

        pass


class TwoThreeNode:
    __slots__ = ("keyList", "keyCount", "childList", "parentNode")

    def __init__(self, keyList=None, childList=None, parentNode=None):
        self.keyList = list(keyList) if keyList is not None else []
        self.keyCount = len(self.keyList)

        self.childList = list(childList) if childList is not None else []
        self.parentNode = parentNode

        if self.childList:
            for childNode in self.childList:
                childNode.parentNode = self

    def GetKeyCount(self):
        self.keyCount = len(self.keyList)
        return self.keyCount

    def IsLeaf(self):
        return len(self.childList) == 0

    def IsOverflow(self):
        return self.GetKeyCount() == 3

    def InsertKey(self, keyValue):
        self.keyList.append(keyValue)
        self.keyList.sort()
        self.GetKeyCount()
        return self.keyList.index(keyValue)

    def ChildIndexFor(self, keyValue):
        indexValue = 0
        while indexValue < self.GetKeyCount() and keyValue >= self.keyList[indexValue]:
            indexValue += 1
        return indexValue

    def SetChildren(self, childList):
        self.childList = list(childList)
        for childNode in self.childList:
            childNode.parentNode = self


class TwoThreeTree(AbstractSearchInterface):

    def __init__(self, stringValue):
        self.rootNode = None
        if stringValue is not None:
            for elementValue in stringValue:
                self.insertElement(elementValue)

    def insertElement(self, elementValue):
        inserted = False

        if self.rootNode is None:
            self.rootNode = TwoThreeNode([elementValue])
            return True

        # traverse to leaf
        currentNode = self.rootNode
        while not currentNode.IsLeaf():
            childIndexValue = currentNode.ChildIndexFor(elementValue)
            currentNode = currentNode.childList[childIndexValue]

        # insert at leaf
        currentNode.InsertKey(elementValue)
        inserted = True

        # fix 4-nodes up the tree
        while currentNode is not None and currentNode.IsOverflow():
            self.SplitNode(currentNode)
            currentNode = currentNode.parentNode

        return inserted

    def searchElement(self, elementValue):
        found = False

        currentNode = self.rootNode
        while currentNode is not None:
            keyIndexValue = 0
            while keyIndexValue < currentNode.keyCount:
                if elementValue == currentNode.keyList[keyIndexValue]:
                    return True
                keyIndexValue += 1

            if currentNode.IsLeaf():
                return False

            childIndexValue = currentNode.ChildIndexFor(elementValue)
            currentNode = currentNode.childList[childIndexValue]

        return found

    def SplitNode(self, overflowNode):
        # overflow (4 nodes) have 3 keys
        keyA = overflowNode.keyList[0]
        keyB = overflowNode.keyList[1]  # promoted
        keyC = overflowNode.keyList[2]

        leftNode = TwoThreeNode([keyA])
        rightNode = TwoThreeNode([keyC])

        # Reattach children if internal
        if overflowNode.childList:
            leftChildren = [overflowNode.childList[0], overflowNode.childList[1]]
            rightChildren = [overflowNode.childList[2], overflowNode.childList[3]]
            leftNode.SetChildren(leftChildren)
            rightNode.SetChildren(rightChildren)

        parentNode = overflowNode.parentNode

        # create new node
        if parentNode is None:
            newRootNode = TwoThreeNode([keyB], [leftNode, rightNode], None)
            self.rootNode = newRootNode
            return

        # overflow push to parent and replace children with 2 nodes
        overflowIndexValue = 0
        while (
            overflowIndexValue < len(parentNode.childList)
            and parentNode.childList[overflowIndexValue] is not overflowNode
        ):
            overflowIndexValue += 1

        if overflowIndexValue == len(parentNode.childList):
            raise ValueError("Parent does not reference overflow child.")

        # Insert promoted key into parent
        _ = parentNode.InsertKey(keyB)

        #replace children
        parentNode.childList.pop(overflowIndexValue)
        parentNode.childList.insert(overflowIndexValue, leftNode)
        parentNode.childList.insert(overflowIndexValue + 1, rightNode)
        leftNode.parentNode = parentNode
        rightNode.parentNode = parentNode

        self.NormalizeChildrenOrder(parentNode)

    def NormalizeChildrenOrder(self, parentNode):
        #sort children
        if not parentNode.childList:
            return

        parentNode.childList.sort(key=lambda nodeValue: nodeValue.keyList[0])
        for childNode in parentNode.childList:
            childNode.parentNode = parentNode


def PrintSearch(treeValue, elementValue):
    print(
        "searchElement(",
        repr(elementValue),
        ") -> ",
        treeValue.searchElement(elementValue),
        sep="",
    )


def PrintRoot(treeValue):
    if treeValue.rootNode is None:
        print("rootNode: None")
    else:
        print(
            "rootNode.keyList =",
            treeValue.rootNode.keyList,
            "keyCount =",
            treeValue.rootNode.keyCount,
        )
