import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import string
import random

class ResolutionNode():
    def __init__(self, variables, parent, child):
        self.variables = variables
        self.parent = parent
        self.child = child

class ResolutionGraph():
    def __init__(self):
        self.tree_nodes = []

    def addNode(self, variables, parent, child, level):
        if len(self.tree_nodes) < level:
            self.tree_nodes.append([])
        self.tree_nodes[level].append(ResolutionNode(variables, parent, child))


class LogicalProblem():
    def __init__(self, num_variables, num_premises, num_complexity, validity):
        possible_variables = list(string.ascii_uppercase)
        self.num_variables = num_variables
        self.variables = possible_variables[0:num_variables]
        self.num_premises = num_premises
        self.premises = []
        self.num_complexity = num_complexity
        self.validity = validity

        self.resolution_tree = []
    
    def generate_random(self):
        if self.validity:
            self.resolution_tree.append([])
        else:
            temp = []
            for i in range(random.randint(1:self.num_variables)):
                temp.append()
            self.resolution_tree.append()



# Main function for he whole application
class Main_Application():
    def __init__(self, master):
        self.master = master


        self.initiate_gui()
        self.draw()

    def doNothing(self):
        return

    def initiate_gui(self):
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
        self.generate_problem = Button(self.master, command = self.doNothing, text = "Generate", font=('helvetica', 16))
        
        # Button to clear the potential
        self.can_satisfy = Button(self.master, command = self.doNothing, text = "    ", font=('helvetica', 16))

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


        # Draw the button to clear the potential
        self.generate_problem.grid(column = 1, row = 1, columnspan= 1, padx = 10, pady=10)

        self.can_satisfy.grid(column=5, row=1, columnspan=1, pady=10)

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





