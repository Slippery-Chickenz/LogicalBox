## Logical Box v 1.0
Logical Box is a propositional logic problem generator implemented in Python. Logical problems are defined as a set of premises and a conclusion. The program supports valid and invalid problem generation (where valid problems are those which generate a contradiction when the premises are true and the conclusion is false and invalid problems are those that do not). Problems are displayed in Resolution problem format.


# To Use
Users may tailor problems using three variables: number of variables, number of premises, and complexity.
1. Number of variables: the number of atomic statements to be used in problem generation. More variables allow for the generation of more complex problems
2. Number of premises: the number of premises to be generated from all parent clauses. Premises are generated by randomly connecting clauses with logical 'and's, 'or's, and conditionals.
3. The complexity of the problem. Higher complexity yields more tree branches and thus a higher number of clauses.

Clicking the green button on the right switches problem generation from valid to invalid. Clicking the 'Generate' button on the left generates a new random logic problem. Clicking the 'Generate Premises' button regenerates premises for a given logical problem using the same clauses. The 'Generate Premises' button will also generate a display box listing the premises and conclusion. See Release Notes for more information about display sizes and screen resolution.

# Development
Logical Box makes use of the clause structure used in Resolution and Davis-Putnam to generate and represent problems as an inverted tree. The single leaf node represents the solution to a Resolution problem, where an empty clause indicates a contradiction and thus a valid problem and a non-empty clause does not. Each clause outside of the leaf node possesses a parent and child clause. Root nodes have no children and represent clauses derived directly from premises. Given a clause in the tree, subsequent parent clauses are generated on a random basis at each successive level of the tree as a function of the number of desired variables and complexity.

Logical Box utilizes several classes.
1. LogicalProblem.py contains the LogicalProblem class, which encapsulates the entirety of a single problem. It holds data on user input (number of variables, premises, complexity) and randomly generates variables, clauses, and premises based on generated clauses.
2. ResolutionTree.py defines the tree structure of the LogicalProblem class.
3. ResolutionNode.py contains the class implementation of tree nodes, represented in a logical problem as clauses. Each node has a parent and child and supports negation of variables.
4. Connector.py contains the class definition of a logical statement, wherein a left and right side are joined by some logical operator. For example, $A\implies B$ consists of the left side (A), the right side (B), and the operator $\implies$. Random logical operator generation occurs in this class.
5. Variable.py contains the class representation of a symbol/atomic statement.

# Release Notes
1. Logical Box currently does not support biconditional generation
2. Logical Box currently does not support variable distribution and DeMorgans expansion
3. The Tkinter package uses default static pixel sizing to generate dislay boxes. Windows systems use dynamic scaling to display text and images based on device screen size. We recommend setting the application to fullscrean display with a display resolution of 1920 x 1080 (or above) with 100% text scaling.

We hope that this project provides a good starting point for future expansion and robust logic problem generation.

# Contributors
Luke Dyer: 2023

Kathryn Carbone: 2023

Rom Simovitch: 2023