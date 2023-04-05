import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.font as tkFont
import string
import random

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
        if self.num_variables < self.num_complexity:
            print("Too little variables for this complexity.")
            return
        if self.validity:
            self.resolution_tree.addNode([], (-1, 0), -1, 0) # If valid then we start with an empty node
        else:
            if self.num_variables == self.num_complexity:
                print("Too little variables for this complexity for a non-valid problem.")
                return
            self.resolution_tree.addNode(random.sample(self.variables, random.randint(1, self.num_variables - self.num_complexity)), (-1, 0), -1, 0) # If not valid then we start with a node with stuff in it

        all_var_used = False
        # Just temporary set the number of levels of the tree to the complexity so we loop and generate new branches until we get num_complexity levels
        while self.resolution_tree.numLevels() < self.num_complexity or not all_var_used:
            # Double for loop to loop through every node in the 'tree'
            used_vars = self.variables.copy()
            for i in range(self.resolution_tree.numLevels()):
                for j in range(self.resolution_tree.levelSize(i)):
                    current_node = self.resolution_tree.getNode(i,j) # Just to say what the current node is
                    for v in range(len(current_node.getVariables())):
                        for used_v in range(len(used_vars)):
                            if current_node.getVariables()[v].getVariable() == used_vars[used_v].getVariable():
                                del used_vars[used_v]
                                break
                    if len(used_vars) == 0:
                        all_var_used = True
                    if current_node.getParent()[0] == -1 and random.random() < 0.5 and i < self.num_complexity: # If this node has no parents and we git a coin toss then split on this node
                        possibleVar = [] # List of possible variables to split into

                        for var in self.variables: # Get a list of variables that are not in the current node
                            in_node = False
                            for v in range(len(current_node.getVariables())):
                                for used_v in range(len(used_vars)):
                                    if current_node.getVariables()[v].getVariable() == used_vars[used_v].getVariable():
                                        del used_vars[used_v]
                                        break
                                if current_node.getVariables()[v].getVariable() == var.getVariable():
                                    in_node = True

                            if not in_node:
                                possibleVar.append(var)
                        random_var = random.choice(possibleVar).getVariable() # Pick a random variable to add to the split onto the next level
                        next_vars = current_node.getVariables().copy()
                        temp = Variable(random_var, True)
                        next_vars.append(temp)
                        self.resolution_tree.addNode(next_vars, (-1,-1), j, i + 1) # Make the parent nodes each with the new random variable along with the variables form the node we split off oftemp = current_node.getVariables()
                        
                        next_vars = current_node.getVariables().copy()
                        temp = Variable(random_var, False)
                        next_vars.append(temp)
                        self.resolution_tree.addNode(next_vars, (-1,-1), j, i + 1) # Also make the parents nothing and then give it its level and child
                        
                        current_node.changeParent((self.resolution_tree.levelSize(i + 1) - 2, self.resolution_tree.levelSize(i + 1) - 1)) # Set the node we split off of to have the correct parents



# Main function for he whole application
class Main_Application():
    def __init__(self, master):
        self.master = master
        self.problems = []
        self.valid = True

        self.initiate_gui() # Initate all the GUI elements
        self.draw() # Draw all the GUI elements to the window

    def generateProblem(self):
        newProblem = LogicalProblem(int(self.variable_input.get()), int(self.premise_input.get()), int(self.complexity_input.get()), self.valid)
        newProblem.generate_random()
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

    def doNothing(self):
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
        self.variable_input = Spinbox(self.master, from_ = 1, to = 100, font=('helvetica', 20))
        self.variable_input_label = Label(self.master, text = "# of Variables", font=('helvetica', 15))

        
        # Make a text box to input values instead
        self.premise_input = Spinbox(self.master, from_ = 1, to = 100, font=('helvetica', 20))
        self.premise_input_label = Label(self.master, text = "# of Premises", font=('helvetica', 15))


        # Make a textbox to change sizey
        self.complexity_input = Spinbox(self.master, from_ = 1, to = 100, font=('helvetica', 20))
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





