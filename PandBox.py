
from tkinter import *
from LogicalProblem import LogicalProblem


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
        #newProblem.generatePremises()
        newProblem.resolution_tree.printTree()
        self.problems.append(newProblem)
        self.canvas.delete('all')
        self.drawTree(-1)

    def generatePremises(self):
        self.problems[-1].generatePremises(int(self.premise_input.get()))
        return


    def drawTree(self, problem_num):
        problem = self.problems[problem_num]
        tree = problem.getTree()
        tree.organizeTree()
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
                if not (current_node.child == -1):
                     child_dw = 1400/(tree.levelSize(i - 1))
                     self.canvas.create_line(dw*(1/2 + j),100*(tree.numLevels() - i) + 10,child_dw*(1/2 + current_node.child),100*(tree.numLevels() - i + 1) - 10, fill="black", width=3)


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
        self.master.columnconfigure(6, weight =1, minsize=220)


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

        # Button to clear the potential
        self.generate_premises = Button(self.master, command = self.generatePremises, text = "Generate Premises", font=('helvetica', 16))

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

        
        # Draw the button to generate the problem and swap if it is valid
        self.generate_premises.grid(column = 6, row = 1, columnspan= 1, padx = 10, pady=10)

        self.can_satisfy.grid(column=5, row=1, columnspan=1, pady=10)

        # Draw the canvas

        self.canvas.grid(column = 1, row = 3, columnspan= 6)


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

        # Forget the button to generate
        self.generate_premises.grid_forget()


# if __name__ == "__main__": lmao
if __name__ == "__main__" :


    app = Tk()

    everything = Main_Application(app)

    app.mainloop()





