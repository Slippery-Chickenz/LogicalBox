import random

class Premise():
    '''
    class to encapsulate a logical statement defined as
    a left and right side conjoined by a connector
    connector can be three possibilities:
    &, |, -->
    '''
    def __init__(self, clauses):

        self.clauses = clauses


    def addClause(self, clause):
        self.clauses.append(clause)

    def __add__(self, other):
        new_clauses = self.clauses + other.clauses
        return Premise(new_clauses)