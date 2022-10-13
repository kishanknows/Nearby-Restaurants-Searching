class Node():
    def __init__(self, value):
        self.value = value
        self.isleaf = False
        self.left = None
        self.right = None
        self.assoc = None

def Buildassoc(points):
    if(len(points)==0):
        return None
    if(len(points)==1):
        node = Node(points[0])
        node.isleaf = True
        return node
    mid = len(points)//2
    node = Node(points[mid])
    node.left = Buildassoc(points[:mid])
    node.right = Buildassoc(points[mid:])
    return node

def BuildTree2D(points):
    if(len(points)==0):
        return None
    tree = Buildassoc(sorted(points, key = lambda a : a[1]))
    if(len(points)==1):
        node = Node(points[0])
        node.isleaf = True
        node.assoc = tree
        return node
    mid = len(points)//2
    node = Node(points[mid])
    node.left = BuildTree2D(points[:mid])
    node.right = BuildTree2D(points[mid:])
    node.assoc = tree
    return node

def findSplitNode(root, p1, p2, flag):
    if not root:
        return None
    if(p1 < root.value[flag] and p2 < root.value[flag] and root.left):
        return findSplitNode(root.left, p1, p2, flag)
    elif(p1 > root.value[flag] and p2 > root.value[flag] and root.right):
        return findSplitNode(root.right, p1, p2, flag)
    return root

def query1D(root, p1, p2, flag, leafs):
    if not root:
        return
    if root.isleaf:
        if root.value[flag] <= p2 and root.value[flag] >= p1:
            leafs.append(root.value)
        else:
            return
    if p2 < root.value[flag]:
        query1D(root.left, p1, p2, flag, leafs)
    elif p1 > root.value[flag]:
        query1D(root.right, p1, p2, flag, leafs)
    else:
        query1D(root.left, p1, p2, flag, leafs)
        query1D(root.right, p1, p2, flag, leafs)

def query2D(root, p1, p2, p3, p4):
    ans = []
    if not root:
        return ans
    splitnode = findSplitNode(root, p1, p2, 0)
    if not splitnode:
        return ans
    if splitnode.isleaf:
        if splitnode.value[0] <= p2 and splitnode.value[0] >= p1 and splitnode.value[1] <=p4 and splitnode.value[1] >= p3:
            ans.append(splitnode.value)
        else:
            return ans
    else:
        node = splitnode.left
        while not node.isleaf:
            if p1 <= node.value[0] and node.left and node.right:
                query1D(node.right.assoc, p3, p4, 1, ans) 
                node = node.left
            elif node.right:
                node = node.right
        if node.value[0] <= p2 and node.value[0] >= p1 and node.value[1] <= p4 and node.value[1] >= p3:
            ans.append(node.value)
        node = splitnode.right
        while not node.isleaf:
            if p2 >= node.value[0] and node.left and node.right:
                query1D(node.left.assoc, p3, p4, 1, ans) 
                node = node.right
            elif node.left:
                node = node.left
        if node.value[0] <= p2 and node.value[0] >= p1 and node.value[1] <= p4 and node.value[1] >= p3:
            ans.append(node.value)
    return ans

class PointDatabase():
    def __init__(self, pointlist):
        self.data = BuildTree2D(sorted(pointlist, key = lambda a : a[0]))

    def searchNearby(self, q, d):
        return query2D(self.data, q[0]-d, q[0]+d, q[1]-d, q[1]+d)


