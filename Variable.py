class Variable():
    def __init__(self, var_name, truthValue):
        self.var_name = var_name
        self.truthValue = truthValue

    def printVar(self):
        print("~{},".format(self.var_name))
    
    def stringVar(self):
        if self.truthValue:
            return "{}".format(self.var_name)
        return "~{}".format(self.var_name)
    
    def getVariable(self):
        return self.var_name
    
    def getTruthValue(self):
        return self.truthValue
    
    def negateVariable(self):
        self.truthValue = not self.truthValue
    
    def __eq__(self, other):
        if self.var_name == other.var_name and self.truthValue == other.truthValue:
            return True
        return False
