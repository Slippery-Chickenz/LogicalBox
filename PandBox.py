import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.font as tkFont
import string
import random
import copy

class Variable():
    def __init__(self, var_name, truthValue):
        self.var_name = var_name
        self.truthValue = truthValue

    def printVar(self):
        print("~{},".format(self.var_name))
    
    def stringVar(self):
        if self.truthValue:
            return "{}".format(self.var_name)
        return "~{}".format(self.var_name)
    
    def getVariable(self):
        return self.var_name
    
    def __eq__(self, other):
        if self.var_name == other.var_name and self.truthValue == other.truthValue:
            return True
        return False


# Class to hold all the data needed in a node in the tree. This is useful again mostly just to draw the tree (I'm sorry)
class ResolutionNode():
    def __init__(self, variables, parent, child):
        self.variables = variables
        self.parent = parent
        self.child = child

    def getParent(self):
        return self.parent
    
    def getVariables(self):
        return self.variables
    
    def changeParent(self, new_parents):
        self.parent = new_parents

    def printNode(self):
        print("([", end = '')
        for i in self.variables:
            print("{},".format(i.stringVar()), end = '')
        print("],{},{})".format(self.parent, self.child), end = '')
    
    def __eq__(self, other):
        if self.parent == other.parent and self.child == other.child:
            vars_s = self.getVariables()
            vars_o = other.getVariables()
            if len(vars_s)==len(vars_o):
                for i in range(len(vars_s)):
                    if vars_s[i] == vars_o[i]:
                        return True
        return False

# Class to hold the details of the resolution tree (This is mostly necessary because I think it would be nice to draw the tree later and this would help that)
class ResolutionTree():
    def __init__(self):
        self.tree_nodes = [] # Just a list of all the nodes in the tree
        self.total_size = 0
         # This will be a list of lists and each index value for each sub list is the level of the tree with the first one being the 'lowest on the tree' so we start with level 0 as the firstr
         # item in the list and then as we go up the tree to the top where we would normally start that would be the end of the list.

    # Function to add nodes to the tree as a certain level
    def addNode(self, variables, parent, child, level):
        self.total_size += 1
        # If we do not have that level yet then add it
        if len(self.tree_nodes) <= level:
            self.tree_nodes.append([])
        # Add a node to the tree in the proper level
        self.tree_nodes[level].append(ResolutionNode(variables, parent, child))

    def numLevels(self):
        return len(self.tree_nodes)

    def levelSize(self, level):
        return len(self.tree_nodes[level])
    
    def getNode(self, level, num):
        return self.tree_nodes[level][num]
    
    def printTree(self):
        for i in range(len(self.tree_nodes)):
            print("\n")
            for j in range(len(self.tree_nodes[i])):
                self.tree_nodes[i][j].printNode()
                print(", ", end = '')


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
        else:
            if self.num_variables == self.num_complexity:
                print("Too few variables for this complexity for a non-valid problem.")
                return
            init_var = random.sample(self.variables, random.randint(max(1, self.num_variables - num_splits_left), self.num_variables - self.num_complexity))
            used_vars = copy.deepcopy(init_var)
            self.resolution_tree.addNode(init_var, (-1, -1), -1, 0) # If not valid then we start with a node with stuff in it

        all_var_used = False
        # Just temporary set the number of levels of the tree to the complexity so we loop and generate new branches until we get num_complexity levels
        while self.resolution_tree.numLevels() <= self.num_complexity or not all_var_used:
            # Double for loop to loop through every node in the 'tree'
            for i in range(self.resolution_tree.numLevels()):
                for j in range(self.resolution_tree.levelSize(i)):
                    current_node = self.resolution_tree.getNode(i,j) # Just to say what the current node is
                    current_node.printNode()
                    print("")
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

    def generatePremises(self):
        parents = []
        for level in self.resolution_tree.tree_nodes:
            for node in level:
                if node.getParent() == (-1,-1):
                    parents.append([node])
        #print(parents)
        p_ind = random.randrange(len(parents))
        # TODO: Negate premise
        premise = parents.pop(p_ind)
        print(len(parents))
        while True:
            ind_sublist = random.sample(range(0,len(parents)), 2)
            sublist = [parents[ind_sublist[0]],parents[ind_sublist[1]]]
            parents.pop(ind_sublist[0])
            if len(ind_sublist) > 1:
                parents.pop(ind_sublist[1]-1)

            parents.append(sublist)
            if len(parents) <= self.num_premises:
                break
        print(len(parents))
        self.premises = parents + premise

# Main function for he whole application
class Main_Application():
    def __init__(self, master):
        self.master = master
        self.problems = []
        self.valid = True
        self.num_variables = StringVar()
        self.num_variables.set('')
        self.num_complexity = StringVar()
        self.num_complexity.set('')
        self.num_premises = StringVar()
        self.num_premises.set('')

        self.initiate_gui() # Initate all the GUI elements
        self.draw() # Draw all the GUI elements to the window

    def generateProblem(self):
        newProblem = LogicalProblem(int(self.variable_input.get()), int(self.premise_input.get()), int(self.complexity_input.get()), self.valid)
        newProblem.generate_random()
        newProblem.generatePremises()
        newProblem.resolution_tree.printTree()
        self.problems.append(newProblem)
        self.canvas.delete('all')
        self.drawTree(-1)


    def drawTree(self, problem_num):
        problem = self.problems[problem_num]
        tree = problem.getTree()
        for i in range(tree.numLevels()):
            for j in range(tree.levelSize(i)):
                current_node = tree.getNode(i,j) # Just to say what the current node is
                node_text = '{'
                current_variables = current_node.getVariables()
                for var in current_variables:
                    node_text += var.stringVar() + ','
                if len(node_text) > 1:
                    node_text = node_text[:-1]
                node_text += '}'
                dw = 1400/(tree.levelSize(i))
                self.canvas.create_text(dw*(1/2 + j), 100*(tree.numLevels() - i), text= node_text, fill = 'black', font = ("TkFixedFont", 16))


    def swapValidity(self):
        self.valid = not self.valid

        if self.valid:
            self.can_satisfy = Button(self.master, command = self.swapValidity, text = "    ", bg = 'green', font=('helvetica', 16))
            self.can_satisfy.grid(column=5, row=1, columnspan=1, pady=10)

        else:
            self.can_satisfy = Button(self.master, command = self.swapValidity, text = "    ", bg = 'red', font=('helvetica', 16))
            self.can_satisfy.grid(column=5, row=1, columnspan=1, pady=10)

    # Function to force the complexity to be within a certain range depending on the number of variables
    def updateComplexity(self, a, b, c):
        var_input = int(self.variable_input.get()) # Get the current number of variables
        n = 0 # This will be the minimum complexity
        S = 1 # Just a dummy
        while var_input >= S: # While the number of variables is less than 2^n we add 1 to n
            n += 1
            S = 2**n
        # All of the crap in this if statement below is just to make sure the UI doesnt let you have non-possible complexity values for any given number of variables if you want non-valid answers
        if not self.valid: # If we want a non-valid problem we can have less complexity
            n = 1
            self.num_complexity.set(str(n)) # This is just resetting the complexity gui element to add the new min max
            self.complexity_input.grid_forget()
            if (var_input == 1):
                self.complexity_input = Spinbox(self.master, from_ = n, to = 1, textvariable=self.num_complexity, font=('helvetica', 20))
                self.complexity_input.grid(column = 4, row = 1, columnspan= 1, padx = 10, pady=10)
            else:
                self.complexity_input = Spinbox(self.master, from_ = n, to = var_input - 1, textvariable=self.num_complexity, font=('helvetica', 20))
                self.complexity_input.grid(column = 4, row = 1, columnspan= 1, padx = 10, pady=10)
            return
        # This works because at each n level in a tree you can have up to possibly 2^n variables and you can also have n variables you can also make n levels
        self.num_complexity.set(str(n)) # This is just resetting the complexity gui element to add the new min max
        self.complexity_input.grid_forget()
        self.complexity_input = Spinbox(self.master, from_ = n, to = var_input, textvariable=self.num_complexity, font=('helvetica', 20))
        self.complexity_input.grid(column = 4, row = 1, columnspan= 1, padx = 10, pady=10)
        return

    def initiate_gui(self):

        # Forcing different columns to be set width for the UI so it can only get so small
        self.master.columnconfigure(1, weight =1, minsize=150)
        self.master.columnconfigure(2, weight =1, minsize=150)
        self.master.columnconfigure(3, weight =1, minsize=150)
        self.master.columnconfigure(4, weight =1, minsize=150)
        self.master.columnconfigure(5, weight =1, minsize=50)
        self.master.columnconfigure(6, weight =1)


        # Make a text box to input values instead
        self.variable_input = Spinbox(self.master, from_ = 1, to = 100, textvariable=self.num_variables, font=('helvetica', 20))
        self.variable_input_label = Label(self.master, text = "# of Variables", font=('helvetica', 15))

        self.num_variables.trace('w', self.updateComplexity)

        
        # Make a text box to input values instead
        self.premise_input = Spinbox(self.master, from_ = 1, to = 100, font=('helvetica', 20))
        self.premise_input_label = Label(self.master, text = "# of Premises", font=('helvetica', 15))


        # Make a textbox to change sizey
        self.complexity_input = Spinbox(self.master, from_ = 1, to = 100, textvariable=self.num_complexity, font=('helvetica', 20))
        self.complexity_label = Label(self.master, text = "'Complexity'", font=('helvetica', 15))
        
        # Button to clear the potential
        self.generate_problem = Button(self.master, command = self.generateProblem, text = "Generate", font=('helvetica', 16))
        
        # Button to clear the potential
        self.can_satisfy = Button(self.master, command = self.swapValidity, text = "    ", bg = 'green', font=('helvetica', 16))

        # Canvas to draw the tree onto
        self.canvas = Canvas(self.master, bg="SpringGreen2", width= 1400, height = 750)

    def draw(self):
        
        # Draw variable_input
        self.variable_input.grid(column = 2, row = 1, columnspan= 1, padx = 10, pady=10)
        self.variable_input_label.grid(column = 2, row = 0, columnspan= 1)   

        
        # Draw premise_input
        self.premise_input.grid(column = 3, row = 1, columnspan= 1, padx = 10, pady=10)
        self.premise_input_label.grid(column = 3, row = 0, columnspan= 1)
          

        # Draw the sizey input and label
        self.complexity_input.grid(column = 4, row = 1, columnspan= 1, padx = 10, pady=10)
        self.complexity_label.grid(column = 4, row = 0, columnspan= 1)


        # Draw the button to generate the problem and swap if it is valid
        self.generate_problem.grid(column = 1, row = 1, columnspan= 1, padx = 10, pady=10)

        self.can_satisfy.grid(column=5, row=1, columnspan=1, pady=10)

        # Draw the canvas

        self.canvas.grid(column = 1, row = 3, columnspan= 5)


        return

    def forget(self):

        
        # Forget variable_input
        self.variable_input.grid_forget()
        self.variable_input_label.grid_forget()   

        # Forget premise_input
        self.premise_input.grid_forget()
        self.premise_input_label.grid_forget()


        # Forget the complexity input and label
        self.complexity_input.grid_forget()
        self.complexity_label.grid_forget()

        # Forget the satisfiablility button
        self.can_satisfy.grid_forget()

        # Forget the button to generate
        self.generate_problem.grid_forget()



# if __name__ == "__main__": lmao
if __name__ == "__main__" :


    app = Tk()

    everything = Main_Application(app)

    app.mainloop()





