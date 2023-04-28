import random
import string
import copy

from Variable import Variable
from ResolutionTree import ResolutionTree
from ResolutionNode import ResolutionNode
from Connector import Connector

class LogicalProblem():
    '''
    Class to hold a single logical problem and functions that will act on it
    num_variables: user input: number of variables to appear in problem
    variables: list of variables
    num_premises: number of premises
    premises: list of premises by clause
    connector: list of premises by connectors
    num_complexity: determines how often to branch
    validity: valid/invalid flag
    resolution_tree: holds tree for problem
    '''

    def __init__(self, num_variables, num_premises, num_complexity, validity):
        possible_variables = list(string.ascii_uppercase)
        self.num_variables = num_variables
        self.variables = []
        for i in range(num_variables):
            self.variables.append(Variable(possible_variables[i], True))
        self.num_premises = num_premises
        self.premises = []
        self.num_possible_premises = 0
        self.connector = []
        self.num_complexity = num_complexity
        self.validity = validity

        self.resolution_tree = ResolutionTree()


    def getTree(self):
        return self.resolution_tree
    
    def getConnectors(self):
        return self.connector
    
    #Main function to generate random logical problem
    def generate_random(self):
        used_vars = [] # List to keep track of what variables we have used so far in this tree
        num_splits_left = 2**self.num_complexity - 1

        ### ERROR CHECKING
        if self.num_variables < self.num_complexity:
            print("Too few variables for this complexity.")
            return
        if self.validity:
            self.resolution_tree.addNode([], (-1, -1), -1, 0) # If valid then we start with an empty node
        else: # If not valid then we must generate a startin node with variables in it
            if self.num_variables == self.num_complexity:
                print("Too few variables for this complexity for a non-valid problem.")
                return
            
            init_var = random.sample(self.variables, random.randint(max(1, self.num_variables - num_splits_left), self.num_variables - self.num_complexity)) # Sample of some random variables
            used_vars = copy.deepcopy(init_var) # Note which variables are used
            for v in init_var: # Choose them at random to be negations
                if random.random() < 0.5:
                    v.truthValue = not v.truthValue
            self.resolution_tree.addNode(init_var, (-1, -1), -1, 0) # Start the tree with a node of our random variables

        ### PROBLEM GENERATION
        all_var_used = False
        # Temporarily set the number of levels of the tree to the complexity
        # Loop and generate new branches until we get num_complexity levels
        while self.resolution_tree.numLevels() <= self.num_complexity or not all_var_used:
            # Loop through every node in the 'tree'
            for i in range(self.resolution_tree.numLevels()):
                for j in range(self.resolution_tree.levelSize(i)):
                    current_node = self.resolution_tree.getNode(i,j) # Just to say what the current node is
                    if len(used_vars) == len(self.variables):
                        all_var_used = True

                    #If node has no parents, check whether to split
                    if current_node.getParent()[0] == -1 and random.random() < 0.5 and i < self.num_complexity:
                        possibleVar = [] # Possible variables to split on
                        for var in self.variables: # Get a list of variables that we could split with
                            in_node = False
                            #Check whether to choose unused variables to split on 
                            if num_splits_left <= (self.num_variables - len(used_vars)):
                                for v in range(len(used_vars)): # Loop through all the used variables
                                    if used_vars[v].getVariable() == var.getVariable():
                                        in_node = True
                                
                                if not in_node:
                                    possibleVar.append(var)
                            else: # If we do have enough splits left for the total number of variables then we can just split on any variable not in the node we are splitting off of
                                for v in range(len(current_node.getVariables())):
                                    if current_node.getVariables()[v].getVariable() == var.getVariable(): # If variable in current node raise flag
                                        in_node = True

                                if not in_node: # If the variable is not in the current node then we can possibly split off of it
                                    possibleVar.append(var)
                        if len(possibleVar) == 0: # If the node already uses all the variables don't try to split
                            continue
                        random_var = random.choice(possibleVar) # Pick a random variable to add to the split onto the next level
                        if random_var not in used_vars:
                            used_vars.append(random_var)
                        next_vars_true = []
                        next_vars_false = []
                        for var in current_node.getVariables():
                            if random.random() < 0.5:
                                next_vars_true.append(var)
                                if random.random() < 0.5: # Maybe this one changes
                                    next_vars_false.append(var)
                            else:
                                next_vars_false.append(var)
                                if random.random() < 0.5: # Maybe this one changes
                                    next_vars_true.append(var)
                        next_vars_true.append(Variable(random_var.getVariable(), True))
                        next_vars_false.append(Variable(random_var.getVariable(), False))
                        self.resolution_tree.addNode(next_vars_true, (-1,-1), j, i + 1) # Initialize new nodes
                        self.resolution_tree.addNode(next_vars_false, (-1,-1), j, i + 1)

                        num_splits_left -= 1
                        
                        #update parents of current node
                        current_node.changeParent((self.resolution_tree.levelSize(i + 1) - 2, self.resolution_tree.levelSize(i + 1) - 1))

    def getNumPossiblePremises(self):
        n = 0
        for level in self.resolution_tree.tree_nodes:
            for node in level:
                if node.getParent() == (-1,-1):
                    n += 1
        return n


    #main function to combine nodes into premises
    def generatePremises(self, num_premises):
        
        self.premises = []
        self.num_premises = num_premises
        elders = []
        #append parents to list
        for level in self.resolution_tree.tree_nodes:
            for node in level:
                if node.getParent() == (-1,-1):
                    elders.append([copy.deepcopy(node)])
        # TODO: Negate premise
        while True:
            #one of elders will be premise
            if len(elders) <= self.num_premises + 1:
                break
            #randomly select twot clauses to combine
            ind_sublist = random.sample(range(0,len(elders)), 2)
            sublist = elders.pop(ind_sublist[0]) + elders.pop(ind_sublist[1] - 1)
            elders.append(sublist)
        self.premises = elders
        random.shuffle(self.premises)

        #immediately generate connectors for premises
        self.generateConnectors()
    
    # function to generate premise connectors
    def generateConnectors(self):
        self.connector = []
        for prem in self.premises:
            self.connector.append(Connector(copy.deepcopy(prem), True))
            print("\n PREMISE <", end = '')
            for nod in prem:
                nod.printNode(False)
            print(">\n CONNECTOR")
            self.connector[-1].printCon()

        #last element of connector list is conclusion so negate
        print("This boi")
        self.connector[-1].printCon()
        self.connector[-1].negateStatement()
        return

