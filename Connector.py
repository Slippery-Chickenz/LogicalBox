import random
from Variable import Variable
from ResolutionNode import ResolutionNode
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
    def __init__(self, premise):
        self.str = ''
        self.connector = '|'
        self.flag = 0
        self.left = []
        self.right = []
        #if only given a single premise
        if premise.getLength() == 1:
            clause = premise.getClause(0)
            #if an atom
            if clause.isAtom():
                self.connector = ' & '
                self.left = clause.getVariables()[0]
                self.right = clause.getVariables()[0]
                #self.str = clause.getVariables()[0].stringVar() + self.connector + clause.getVariables()[0].stringVar()
            #otherwise, randomly generate connector
            '''
            else:
                vars = clause.getVariables()
                num = random.randint(0, len(vars)-1)
                left = ResolutionNode(vars[0:num], clause.getParent(), clause.child)
                right = ResolutionNode(vars[num:], clause.getParent(), clause.child)

                connector, flag = self.RNG()
                self.connector = connector
                self.flag = flag
                if connector == '&':
                    print("&")
                    pass
                    #demorg
                elif connector == '-->':
                    print("-->")
                    #demorg LHS
                    pass
                else:
                    print("|")

                self.left = self.recursiveInit(left)
                self.right = self.recursiveInit(right)
            '''
            self.left = self.recursiveInit(premise)
            self.right = self.recursiveInit(premise)

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
            '''
            else:
                vars = clause.getVariables()
                left = []
                right = []
                if len(vars) == 2:
                    left = ResolutionNode(vars[0], clause.getParent(), clause.child)
                    right = ResolutionNode(vars[1], clause.getParent(), clause.child)
                else:
                    num = random.randint(0, len(vars)-1)
                    left = ResolutionNode(vars[0:num], clause.getParent(), clause.child)
                    right = ResolutionNode(vars[num:], clause.getParent(), clause.child)

                connector, flag = self.RNG()
                self.connector = connector
                self.flag = flag
                if connector == '&':
                    print("&")
                    pass
                    #demorg
                elif connector == '-->':
                    print("-->")
                    #demorg LHS
                    pass
                else:
                    print("|")

                self.left = self.recursiveInit(left)
                self.right = self.recursiveInit(right)
            '''    
        else:
            if len(premise) == 1:
                left = []
                right = []
                if len(vars) == 2:
                    left = ResolutionNode(vars[0], clause.getParent(), clause.child)
                    right = ResolutionNode(vars[1], clause.getParent(), clause.child)
                else:
                    num = random.randint(0, len(vars)-1)
                    left = ResolutionNode(vars[0:num], clause.getParent(), clause.child)
                    right = ResolutionNode(vars[num:], clause.getParent(), clause.child)

            num = random.randint(0, len(premise)-1)
            print(num)
            left = premise[0:num]
            right = premise[num:]

            connector, flag = self.RNG()
            self.connector = connector
            self.flag = flag
            if connector.equals('|'):
                pass
                #demorg
            elif connector.equals('-->'):
                #demorg LHS
                pass
            self.left = self.recursiveInit(left)
            self.left = self.recursiveInit(right)