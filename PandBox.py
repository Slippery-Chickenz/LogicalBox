from tokenize import Double
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib import cm
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib.ticker import MultipleLocator
import math
#from pyparsing import PositionToken
from scipy import integrate




# Main function for he whole application
class Main_Application():
    def __init__(self, master):
        self.master = master
        self.nothing = ''
        
        self.master.columnconfigure(1, weight =1, minsize=150)
        self.master.columnconfigure(2, weight =1, minsize=150)
        self.master.columnconfigure(3, weight =1, minsize=150)
        self.master.columnconfigure(4, weight =1, minsize=150)
        self.master.columnconfigure(5, weight =1, minsize=50)
        self.master.columnconfigure(6, weight =1)


        # Make a text box to input values instead
        self.variable_input = Spinbox(self.master, textvariable = "0.0", font=('helvetica', 20))
        self.variable_input_label = Label(self.master, text = "# of Variables", font=('helvetica', 15))

        
        # Make a text box to input values instead
        self.premise_input = Spinbox(self.master, textvariable = "0.0", font=('helvetica', 20))
        self.premise_input_label = Label(self.master, text = "# of Premises", font=('helvetica', 15))


        # Make a textbox to change sizey
        self.complexity_input = Spinbox(self.master, textvariable = self.nothing, font=('helvetica', 20))
        self.complexity_label = Label(self.master, text = "'Complexity'", font=('helvetica', 15))


        
        # Button to clear the potential
        self.generate_problem = Button(self.master, command = self.doNothing, text = "Generate", font=('helvetica', 16))
        
        # Button to clear the potential
        self.can_satisfy = Button(self.master, command = self.doNothing, text = "    ", font=('helvetica', 16))

        self.draw()

    def doNothing(self):
        return


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
