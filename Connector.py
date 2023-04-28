import random
from Variable import Variable
from ResolutionNode import ResolutionNode
from Premise import Premise

class Connector():
    '''
    class to encapsulate a logical statement defined as
    a left and right side conjoined by a connector
    connector can be three possibilities:
    &, |, -->
    '''


    #case 1: one clause, is atom
        #just connect w/ and
    #case 2: one clause, is not atom
        #split into left and right and recurse
    #case 3: multiple clauses


    #takes in a list of clauses
    def __init__(self, premise, flag):
        self.str = ''
        self.connector = '|'
        self.flag = flag
        self.left = []
        self.right = []
        self.recursiveInit(premise)

    def RNG(self):
        coin_flip = random.random()
        self.flag = 1
        if coin_flip <= 0.33:
            return '&', 0
        elif coin_flip > 0.33 and coin_flip <= 0.66:
            return '|', 1
        else:
            return '-->', 1
        
    def printCon(self):
        print(self.str)
    
    def recursiveInit(self, premise):
        #base case: single variable
        if premise.getLength() == 1:
            clause = premise.getClause(0)
            #if an atom
            if clause.isAtom():
                return

        else:
            if premise.getLength() == 1:
                left = []
                right = []
                clause = premise[0].getClause(0)
                vars = clause.getVariables()
                num = random.randint(1, len(vars)-1)
                left = Premise([ResolutionNode(vars[0:num], clause.getParent(), clause.child)])
                right = Premise[ResolutionNode(vars[num:], clause.getParent(), clause.child)]
            else:
                self.connector = '&'
                num = random.randint(1, len(premise)-1)
            #print(num)
                left = premise[0:num]
                right = premise[num:]

            connector, flag = self.RNG()

            if self.connector == '|':
                if flag == 0:
                    self.flag = not self.flag
            elif self.connector == '&':
                if flag == 1:
                    self.flag = not self.flag
            elif self.connector == '-->':
                #demorg LHS
                pass
            self.left = Connector(left)
            self.left = Connector(right)