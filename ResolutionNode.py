from Variable import Variable

# Class to hold all the data needed in a node in the tree. This is useful again mostly just to draw the tree (I'm sorry)
class ResolutionNode():
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

    def invertVariables(self):
        for var in self.variables:
            var.negateVariable()

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