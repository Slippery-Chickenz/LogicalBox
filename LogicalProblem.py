import random
import string
import copy

from Variable import Variable
from ResolutionTree import ResolutionTree
from Premise import Premise
from ResolutionNode import ResolutionNode

# Class to hold a single logical problem and functions that will act on it
class LogicalProblem():
    def __init__(self, num_variables, num_premises, num_complexity, validity):
        possible_variables = list(string.ascii_uppercase) # Just the uppper case characters to start for our possible variable names
        self.num_variables = num_variables # Just the number of variables in this problem
        self.variables = [] # Just a list of the variables names we will use in this problem
        for i in range(num_variables):
            self.variables.append(Variable(possible_variables[i], True))
        self.num_premises = num_premises # Number of premises in this problem
        self.premises = [] # List of all the premises
        self.num_complexity = num_complexity # Complexity number for the problem
        self.validity = validity # True or false if this problem is valid or not

        self.resolution_tree = ResolutionTree() # To hold the resolution tree used to generate this problem

    def getTree(self):
        return self.resolution_tree
    
    def generate_random(self):
        used_vars = [] # List to keep track of what variables we have used so far in this tree
        num_splits_left = 2**self.num_complexity - 1
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

        all_var_used = False
        # Just temporary set the number of levels of the tree to the complexity so we loop and generate new branches until we get num_complexity levels
        while self.resolution_tree.numLevels() <= self.num_complexity or not all_var_used:
            # Double for loop to loop through every node in the 'tree'
            for i in range(self.resolution_tree.numLevels()):
                for j in range(self.resolution_tree.levelSize(i)):
                    current_node = self.resolution_tree.getNode(i,j) # Just to say what the current node is
                    if len(used_vars) == len(self.variables):
                        all_var_used = True

                    if current_node.getParent()[0] == -1 and random.random() < 0.5 and i < self.num_complexity: # If this node has no parents and we git a coin toss then split on this node
                        possibleVar = [] # List of possible variables to split into
                        for var in self.variables: # Get a list of variables that we could split with
                            in_node = False # To tell if the variable is in the node
                            if num_splits_left <= (self.num_variables - len(used_vars)): # If we don't have enough splits left for the number of variables then we must choose variables to split from that we havn't used yet
                                for v in range(len(used_vars)): # Loop through all the used variables
                                    if used_vars[v].getVariable() == var.getVariable(): # If the current var from the total list of variables is already used then say its in the node
                                        in_node = True
                                
                                if not in_node: # If its not in the node (therefore its not used yet) then append it to the possible vars we can split from
                                    possibleVar.append(var)
                            else: # If we do have enough splits left for the total number of variables then we can just split on any variable not in the node we are splitting off of
                                for v in range(len(current_node.getVariables())): # Loop through all the variables in the node we are splitting from 
                                    if current_node.getVariables()[v].getVariable() == var.getVariable(): # If the variable is in teh current node then set it to true
                                        in_node = True

                                if not in_node: # If the variable is not in the current node then we can possibly split off of it
                                    possibleVar.append(var)
                        if len(possibleVar) == 0: # If the node already uses all the variables don't try to split
                            continue
                        random_var = random.choice(possibleVar) # Pick a random variable to add to the split onto the next level
                        if random_var not in used_vars: # If the next random variable is not already used then add it to the used vars
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
                        self.resolution_tree.addNode(next_vars_true, (-1,-1), j, i + 1) # Make the parent nodes each with the new random variable along with the variables form the node we split off oftemp = current_node.getVariables()
                        self.resolution_tree.addNode(next_vars_false, (-1,-1), j, i + 1) # Also make the parents nothing and then give it its level and child

                        num_splits_left -= 1
                        
                        current_node.changeParent((self.resolution_tree.levelSize(i + 1) - 2, self.resolution_tree.levelSize(i + 1) - 1)) # Set the node we split off of to have the correct parents



    # function to generate premise connectors as a function of complexity
    def generateConnectors(self):
        vara = Variable('A', True)
        varb = Variable('B', True)
        varc = Variable('C', True)
        #con = Connector(vara)
        nodea = ResolutionNode([vara,varb], (-1,-1), 0)
        nodeb = ResolutionNode([varc, vara], (-1,-1), 0)
        premise = Premise([nodea, nodeb])
        #con = Connector([nodea, nodeb])
        return

    #main function to combine nodes into premises
    def generatePremises(self):
        elders = []
        for level in self.resolution_tree.tree_nodes:
            for node in level:
                if node.getParent() == (-1,-1):
                    elders.append(Premise([node]))
        # TODO: Negate premise
        while True:
            ind_sublist = random.sample(range(0,len(elders)), 2)
            sublist = elders.pop(ind_sublist[0]) + elders.pop(ind_sublist[1] - 1)
            elders.append(sublist)
            if len(elders) <= self.num_premises:
                break
        print(elders)
        self.premises = elders
