import random
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
    def __init__(self, premise, flag):
        self.str = ''
        self.connector = '|'
        self.flag = flag
        self.left = []
        self.right = []
        self.recursiveInit(premise)

    def RNG(self):
        coin_flip = random.random()
        if coin_flip <= 0.33:
            return '&', 0
        elif coin_flip > 0.33 and coin_flip <= 0.66:
            return '|', 1
        else:
            return '-->', 1
        
    def printCon(self):
        print(self.str)

    def getString(self):
        return self.str
    
    def recursiveInit(self, premise):
        #base case: single variable
        if len(premise) == 1:
            clause = premise[0]
            #if an atom
            if clause.isAtom():
                self.left = clause.getVariables()
                self.right = clause.getVariables()
                self.connector = "&"
                if not self.flag:
                    clause.getVariables()[0].negateVariable()
                self.str = clause.getVariables()[0].stringVar()
                return
            
            left = []
            right = []
            clause = premise[0]
            vars = clause.getVariables()
            num = random.randint(1, len(vars)-1)
            left = [ResolutionNode(vars[0:num], clause.getParent(), clause.child)]
            right = [ResolutionNode(vars[num:], clause.getParent(), clause.child)]

        else:
            self.connector = '&'
            num = random.randint(1, len(premise)-1)
        #print(num)
            left = premise[0:num]
            right = premise[num:]

        connector, flag = self.RNG()
        left_flag = True
        right_flag = True
        if self.connector == '|':
            if flag == 0:
                self.flag = not self.flag
                left_flag = not left_flag
                right_flag = not right_flag
            elif connector == "-->":
                left_flag = not left_flag
        elif self.connector == '&':
            if flag == 1:
                self.flag = not self.flag
                if connector == '|':
                    left_flag = not left_flag
                    right_flag = not right_flag
                else:
                    right_flag = not right_flag
        self.connector = connector
        self.left = Connector(left, left_flag)
        self.right = Connector(right, right_flag)
        self.str = "(" + self.left.getString() + self.connector + self.right.getString() + ") "
        if self.flag:
            self.str = " " + self.str
        else:
            self.str = " ~" + self.str
