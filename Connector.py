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
    #takes in a list of clauses
    def __init__(self, premise):
        if premises.getLength() == 1:
            #assumes return of list type
            node = premises.getPremise()[0]











            #return premises
        elif isinstance(premises, ResolutionNode):
            num = random.randint(len(premises.variables)-1)
            left = premises.variables[0:num]
            right = premises.variables[num:]

            connector, flag = self.RNG()
            self.conn = connector
            self.flag = flag
            if connector.equals('&'):
                pass
                #demorg
            elif connector.equals('-->'):
                #demorg LHS
                pass
            #self.left = self.recursiveInit(left)
            #self.left = self.recursiveInit(right)
            return 
        '''
        self.left = self.recursiveInit(premises)
        self.right = recursiveInit(premises)

        num = random.randint(len(premises)-1)
        left = premises[0:num]
        right = premises[num:]
        coin_flip = random.random()
        self.flag = 1
        if coin_flip <= 0.33:
            self.conn = '&'
            self.flag = 0
        elif coin_flip > 0.33 and coin_flip <= 0.66:
            self.conn = '|'
            #demorg both sides
        else:
            self.conn = '-->'
            #demorg right side
        self.left = Connector(left)
        self.right = Connector(right)

        pass
    
    def RNG(self):
        coin_flip = random.random()
        self.flag = 1
        if coin_flip <= 0.33:
            return '&', 0
        elif coin_flip > 0.33 and coin_flip <= 0.66:
            return '|', 1
        else:
            return '-->', 1
    
    def recursiveInit(self, premises):
        #base case: single variable
        if isinstance(premises, Variable):
            print("is variable!")
            return premises
            #return premises
        elif isinstance(premises, ResolutionNode):
            num = random.randint(len(premises.variables)-1)
            left = premises.variables[0:num]
            right = premises.variables[num:]

            connector, flag = self.RNG()
            self.conn = connector
            self.flag = flag
            if connector.equals('&'):
                pass
                #demorg
            elif connector.equals('-->'):
                #demorg LHS
                pass
            self.left = self.recursiveInit(left)
            self.left = self.recursiveInit(right)
            return 
            #return premises
        #recursive call
        #split premises into two sublists
        
        num = random.randint(len(premises)-1)
        left = premises[0:num]
        right = premises[num:]

        connector, flag = self.RNG()
        self.conn = connector
        self.flag = flag
        if connector.equals('|'):
            pass
            #demorg
        elif connector.equals('-->'):
            #demorg LHS
            pass
        self.left = self.recursiveInit(left)
        self.left = self.recursiveInit(right)
        return 
        self.left = Connector(left)
        self.right = Connector(right)
'''