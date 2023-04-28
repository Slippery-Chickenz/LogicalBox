from Connector import Connector
from ResolutionNode import ResolutionNode
class Premise():
    '''
    class to encapsulate a logical statement defined as
    a left and right side conjoined by a connector
    connector can be three possibilities:
    &, |, -->
    '''
    def __init__(self, clauses):

        self.clauses = clauses
       # self.connector

    def getLength(self):
        return len(self.clauses)
    
    def getClauseLength(self, cindex):
        return len(self.clauses[cindex])
    
    def getClause(self, cindex):
        return self.clauses[cindex]

    def addClause(self, clause):
        self.clauses.append(clause)

    def generateConnector(self):
        self.connector = Connector(self)

    def printPremise(self):
        print("[", end = '')
        for clause in self.clauses:
            clause.printNode(False)
        print("]")
        return

    def negatePremise(self):
        for clause in self.clauses:
            clause.invertVariables()

        new_clauses = []
        if len(self.clauses) == 1:
            for v1 in self.clauses[0].getVariables():
                new_clauses.append(ResolutionNode([v1], (-1, -1), -1))
            return

        claus1 = self.clauses.pop(0)
        claus2 = self.clauses.pop(0)
        for v1 in claus1.getVariables():
            for v2 in claus2.getVariables():
                new_clauses.append(ResolutionNode([v1,v2], (-1,-1), -1))

        for nclause in new_clauses:
                nclause.simplifyClause()

        temp = []
        [temp.append(x) for x in new_clauses if x.numVariables() > 0]
        new_clauses = temp
        
        for clause in self.clauses:
            temp_new_clauses = []
            for nclause in new_clauses:
                nclause.simplifyClause()
            
            temp = []
            [temp.append(x) for x in new_clauses if x.numVariables() > 0]
            new_clauses = temp

            for var in clause.getVariables():
                for nclause in new_clauses:
                    temp_Node = ResolutionNode(nclause.getVariables() + [var], (-1, -1), -1)
                    temp_Node.simplifyClause()
                    if temp_Node.numVariables() > 0:
                        temp_new_clauses.append(temp_Node)


            new_clauses = temp_new_clauses

        self.clauses = new_clauses
        

    def __add__(self, other):
        new_clauses = self.clauses + other.clauses
        return Premise(new_clauses)