Graph-Program
=============

It is a program for to make graph theory research!

list of files and what they do:
* icons - pictures for all of the buttons in the interface
* Gui.py - A Tkinter GUI wrapper not specific to this program
* generate.py - Makes the subgraphs that are listed on the right in the GUI, i.e. generates Petersen graphs, Cycles, triangular and hexagonal grids
* graph.py - Graph object used in the program, and necessary Vertex and Edge objects, includes functions to draw the graph and to load adjacency matrices or lists or shortcode from the external Regular Graph Generator
* graphgui.py - the program that starts up the UI and runs the program. Huge, ~2500 lines. includes keyboard controls, handling clicks, rotating, selecting unselecting, Edit Operations: Undo, Redo, Copy, Paste, Connect, Delete, Product commands (Cartesian, Tensor, Strong products), Labeling commands, physics (makes the graph appear aesthetically pleasing on the GUI), File Operations (New, Open, Save, Import, Print, Exit), Whole Graph Commands: Complement, Line Graph, etc.
* graphmath.py - Handles mathematical operations on the graph. Calculates Adjacency matrix, list, or other forms for the graph, calculates tensor products from adjacency matrices, shortest path matrix, Checking labelings, auto labeling, Finds conversion and conversion
* start.py - old starting code that used to pull from a student’s server to get the latest code, using md5checker to check whether the latest code was on the computer. We used github now, so we don’t need to run this ever.
