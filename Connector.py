import random

class Connector():
    '''
    class to encapsulate a logical statement defined as
    a left and right side conjoined by a connector
    connector can be three possibilities:
    &, |, -->
    '''
    def __init__(self, premises):

        #base case

        #recursive call
        #split premises into two sublists
        num = random.randint(len(premises)-1)
        left = premises[0:num]
        right = premises[num:]
        self.conn = '&'
        self.left = Connector(left)
        self.right = Connector(right)

        pass