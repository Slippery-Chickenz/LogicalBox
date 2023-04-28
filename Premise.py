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

    def __add__(self, other):
        new_clauses = self.clauses + other.clauses
        return Premise(new_clauses)