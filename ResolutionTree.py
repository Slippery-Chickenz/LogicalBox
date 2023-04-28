from ResolutionNode import ResolutionNode

# Class to hold the details of the resolution tree (This is mostly necessary because I think it would be nice to draw the tree later and this would help that)
class ResolutionTree():
    '''
    Class to hold resolution tree structure
    tree_nodes: a list of all nodes in the tree
    total_size: a list of lists with each index value for each sub list corresponding to the level of the tree.
                The lowest level (level 0) corresponds to the first sublist.
    '''
    def __init__(self):
        self.tree_nodes = []
        self.total_size = 0


    # Function to add nodes to the tree as a certain level
    def addNode(self, variables, parent, child, level):
        self.total_size += 1
        # If we do not have that level yet then add it
        if len(self.tree_nodes) <= level:
            self.tree_nodes.append([])
        # Add a node to the tree in the proper level
        self.tree_nodes[level].append(ResolutionNode(variables, parent, child))

    def numLevels(self):
        return len(self.tree_nodes)

    def levelSize(self, level):
        return len(self.tree_nodes[level])
    
    def getNode(self, level, num):
        return self.tree_nodes[level][num]
    
    #Function to rearrange tree nodes such that parents are near their children in each subsequent level
    def organizeTree(self):
        for level in range(1, self.numLevels()):
            self.tree_nodes[level] = sorted(self.tree_nodes[level], key = lambda x: x.child)
            for node in range(len(self.tree_nodes[level])):
                if not (self.tree_nodes[level][node].parent == (-1, -1)):
                    self.tree_nodes[level + 1][self.tree_nodes[level][node].parent[0]].child = node
                    self.tree_nodes[level + 1][self.tree_nodes[level][node].parent[1]].child = node

    
    def printTree(self):
        for i in range(len(self.tree_nodes)):
            print("\n")
            for j in range(len(self.tree_nodes[i])):
                self.tree_nodes[i][j].printNode()
                print(", ", end = '')
