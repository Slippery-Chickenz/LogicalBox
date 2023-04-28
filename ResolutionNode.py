from Variable import Variable

class ResolutionNode():
    '''
    Class to hold node data for tree generation. Each node represents a Resolution clause
    variables: a list of variables contained in the clause. Always members of the Variable class
    parent: The ID of a node's parent node. (-1,-1) indicates a root node
    child: The ID of a node's child node.
    '''

    def __init__(self, variables, parent, child):
        self.variables = variables
        self.parent = parent
        self.child = child

    def getParent(self):
        return self.parent
    
    def getVariables(self):
        return self.variables
    
    def numVariables(self):
        return len(self.variables)
    
    def changeParent(self, new_parents):
        self.parent = new_parents

    def printNode(self, par_child = True):
        print("([", end = '')
        for i in self.variables:
            print("{},".format(i.stringVar()), end = '')
        if not par_child:
            print("])", end = '')
            return
        print("],{},{})".format(self.parent, self.child), end = '')

    #Function to negate all variables in a clause
    def invertVariables(self):
        for var in self.variables:
            var.negateVariable()

    #Function to determine whether the clause is an atomic statement
    def isAtom(self):
        if len(self.variables) == 1:
            return True
        return False
    
    def __eq__(self, other):
        if self.parent == other.parent and self.child == other.child:
            vars_s = self.variables
            vars_o = other.getVariables()
            if len(vars_s)==len(vars_o):
                for i in range(len(vars_s)):
                    if vars_s[i] == vars_o[i]:
                        return True
        return False