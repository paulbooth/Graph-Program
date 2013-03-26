#!/usr/bin/python

from decimal import Decimal, getcontext
getcontext.prec = 10
RELATIVE_PREFERENCE_PATH ='preferences.ini'

from copy import copy
import os
import random
import time
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
import pickle
import math
import generate
import graphmath
from copy import deepcopy
from math import *
from Gui import *
from graph import *
import tkColorChooser
try:
    import Image, ImageDraw
except:
    print "no image or imagedraw. :( can't save as images"
    pass
import warnings
try:
    import psyco
except:
    pass
#Graph Types (do we need this?)
PETERSEN = 0
CYCLE = 1
STAR = 2
PRISM = 3
#Graph Commands
CONNECT = 0
MAXUNDO = 100
NUMPHYSICSTYPES=4

myFormats = [('Graph','*.graph')]

class FakeEvent():
    def __init__(self,x,y):
        self.x = x
        self.y = y
class GraphInterface(Gui):
    def __init__(self):
        Gui.__init__(self)
        self.graph = Graph()
        self.ca_width = 600
        self.ca_height = 600
        self.rectangle = ['','']
        self.backups = []
        self.cancelled = False
        self.dragging = False
        self.box = False
        self.handles = {}
        self.clicked_on = None
        self.product_verts=[]
        self.product_edges=[]
        self.click_mode = "vertex"
        #self.clicked_time = 0
        self.copied_verts = []
        self.copied_edges = []
        self.pasting = False
        self.shift_pressed=False
        self.control_pressed = False
        self.attraction=.0005
        self.spacing=10.0
        self.physics_type=0;
        self.stop_physics=True;
        self.area = self.ca_width*self.ca_height
        self.temperature= 100
        self.keep_inbounds = True
        self.kpath = False
        self.tempConversion = False
        self.setup()
        self.mainloop()

        
    def control_up(self, event=None):
        self.control_pressed = False
        self.redraw()

    def control_down(self, event=None):
        self.control_pressed = True
        
    def key(self, event=None):
        print "pressed", repr(event.keysym)
        print "and code", repr(event.keycode)

    def setup(self):
        self.title("Olin Graph Program")
        self.makemenus()
        self.bind("<Key>", self.key)
        #TODO: put in "keybindings" function
        self.bind("<KeyRelease-Control_L>", self.control_up)
        self.bind("<Control_L>", self.control_down)
        self.bind("<KeyRelease-Super_L>", self.control_up)
        self.bind("<Super_L>", self.control_down)
        
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-x>", self.cut)
        self.bind("<Control-v>", self.paste)
        
        self.bind("<Control-n>", self.new)
        self.bind("<Control-s>", self.saveas)
        self.bind("<Control-o>", self.open)
        self.bind("<Control-p>", self.printcanv)
        self.bind("<Control-k>", self.connect)
        self.bind("<Control-l>", self.label_message)
        # self.bind("<Control-r>", self.label_real_message)
        self.bind("<Control-q>", self.clear_labeling)
        self.bind("<Control-u>", self.unlabel_vertex)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Control-b>", self.select_vertices)
        self.bind("<Control-e>", self.select_edges)
        self.bind("<Control-d>", self.deselect_all)
        self.bind("<Control-i>", self.invert_selected)
        self.bind("<Control-r>", self.rotate_selected_message)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-h>", self.toggle_physics)
        self.bind("<Control-f>", self.finishklabeling)
        self.bind("<Control-minus>", self.finishklabeling)
        self.bind("<Control-space>", self.change_cursor)
        #self.bind("<Control-[>",self.box_none)
        #self.bind("<Control-]>",self.box_all)
        # self.bind("<Control-s>", self.snapping)
        # self.bind("<Control-m>", self.curve_selected)
        # self.bind("<Control-w>", self.wrap_selected)
        self.bind("<Control-KeyPress-1>", self.autolabel_easy)
        self.bind("<Control-KeyPress-2>", self.autolabel_easy)
        self.bind("<Control-KeyPress-3>", self.autolabel_easy)
        self.bind("<Control-KeyPress-4>", self.autolabel_easy)
        self.bind("<Control-KeyPress-5>", self.autolabel_easy)
        self.bind("<Control-6>", self.autolabel_easy)
        self.bind("<Control-7>", self.autolabel_easy)
        self.bind("<Control-8>", self.autolabel_easy)
        self.bind("<Control-9>", self.autolabel_easy)
        self.bind("<Control-0>", self.autolabel_easy)
        self.bind("<Delete>", self.delete_selected)
        self.bind("<BackSpace>", self.delete_selected)
        self.bind("<Configure>", self.redraw)
        # self.bind("<Up>", self.curve_height)
        # self.bind("<Down>", self.curve_height)
        self.bind("<KeyPress-F1>", self.helptext)
        self.bind("<Escape>", self.deselect_all)
        self.bind("<Shift_L>",self.shift_down)
        self.bind("<Shift_R>",self.shift_down)
        self.bind("<KeyRelease-Shift_L>", self.shift_up)
##        self.bind("<Up>",self.change_physics)
##        self.bind("<Down>",self.change_physics)
##        self.bind("<Left>",self.change_physics)
##        self.bind("<Right>",self.change_physics)
        
        for i in xrange(10):
            self.bind("<KeyPress-%d>"%i,self.easy_label)
        
        buttons = []
        buttons.append('file')
        buttons.append({'name':'new','image':"new.gif",'command':self.new})
        buttons.append({'name':'open','image':"open.gif",'command':self.open})
        buttons.append({'name':'save','image':"save.gif",'command':self.saveas})
        buttons.append({'name':'print','image':"print.gif",'command':self.printcanv})
        buttons.append('edit')
        buttons.append({'name':'undo','image':"undo.gif",'command':self.undo})
        buttons.append({'name':'redo','image':"redo.gif",'command':self.redo})
        buttons.append({'name':'cut','image':"cut.gif",'command':self.cut})
        buttons.append({'name':'copy','image':"copy.gif",'command':self.copy})
        buttons.append({'name':'paste','image':"paste.gif",'command':self.paste})
        buttons.append('edges')
        buttons.append({'name':'curve','image':"curve.gif",'command':self.curve_selected})
        buttons.append({'name':'connect','image':"connect.gif",'command':self.connect})
        buttons.append({'name':'wrap','image':"wrap.gif",'command':self.wrap_selected})
        buttons.append('physics')
        buttons.append({'name':'start physics','image':"startphy.gif",'command':self.toggle_physics})
        buttons.append({'name':'stop physics','image':"change_physics_type.gif",'command':self.change_physics_type})
        buttons.append('bob')
        
        buttons.append('products')
##        buttons.append(self.cartbutton)
        buttons.append({'name':'Cartesian','image':"cartesian.gif",'command':lambda: self.graph_product('cartesian')})
        buttons.append({'name':'Tensor','image':"tensor.gif",'command':lambda: self.graph_product('tensor')})
        buttons.append({'name':'Strong','image':"strong.gif",'command':lambda: self.graph_product('strong')})
        buttons.append('aesthetics')
        buttons.append({'name':'ColorChooser','image':"colorchooser.gif",'command':self.choose_color})
        buttons.append({'name':'SizePicker','image':"sizepicker.gif",'command':self.pick_size})
        buttons.append({'name':'ShapeSelecter','image':"shapeselecter.gif",'command':self.select_shape})
        self.button_frame= self.fr(LEFT, width=70, expand=0)

        self.menu_buttons(buttons)
        
        #################################################################
        self.fr(TOP, width=32, height=5, bd = 4, bg="grey", expand=0)
        self.endfr()        
        #################################################################
        self.endfr()
        
        self.fr(LEFT, expand = 1)
        self.canvas = self.ca(width=self.ca_width, height=self.ca_height, bg='white')
        # # NOTE: resize works when the canvas is small--could start with this?
        # # NOTE: try to find "minimum size" for resizing entire window, so we can't get any smaller at some me-defined point...keep menus/shit intact.
        #self.canvas = self.ca(width=1, height=1, bg='white')
        #self.canvas.configure(width=self.ca_width, height=self.ca_height)
        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<ButtonRelease-1>", self.released)
        self.canvas.bind("<B1-Motion>", self.dragged)
        self.canvas.bind("<Button-3>", self.right_clicked)
        self.constraintstxt = StringVar()
        self.number_per_circle = StringVar()
        self.grid_size = StringVar()
        self.holes_mode = StringVar()
        self.snap_mode = StringVar()
        self.constraintstxt.set("Labeling Constraints: L(2,1)")
        self.number_per_circle.set("8")
        self.grid_size.set("50")
        self.holes_mode.set("allow")
        self.snap_mode.set("none")
        
        self.fr(TOP, expand = 0)
        self.fr(LEFT, width=2, height=32, bd = 1, bg="grey", expand=0)
        self.endfr()
        self.fr(LEFT)
        self.la(TOP,'both',0,'n',textvariable=self.constraintstxt)
        self.bu(TOP,text="Change",command=self.constraints_message)
        self.endfr()
        self.fr(LEFT, width=2, height=32, bd = 1, bg="grey", expand=0)
        self.endfr()
        self.fr(LEFT)
        self.fr()
        self.endfr()
        self.fr(TOP)
        self.la(LEFT,'both',0,'n',text='Hole Algorithm')
        #TODO: direct "help_holes" to help, with an argument for the section/tag in the help doc.
        self.bu(side = TOP, anchor = W, text="?", command=self.help_holes)
        self.endfr()
        self.widget(Radiobutton,side = TOP, anchor = W, variable=self.holes_mode, text="Allow Holes", value="allow", state="active")
        self.widget(Radiobutton,side = TOP, anchor = W, variable=self.holes_mode, text="Minimize Holes", value="minimize")
        self.widget(Radiobutton,side = TOP, anchor = W, variable=self.holes_mode, text="No Holes", value="none")
        self.endfr()
        self.fr(LEFT, width=2, height=32, bd = 1, bg="grey", expand=0)
        self.endfr()
        self.fr(LEFT)
        self.fr(TOP)
        self.la(TOP,'both',0,'n',text='Snapping')
        self.endfr()
        self.fr(TOP)
        self.fr(LEFT)
        self.widget(Radiobutton,side = TOP, anchor = W, variable=self.snap_mode, text="None", value="none", state="active", command=self.redraw)
        self.widget(Radiobutton,side = TOP, anchor = W, variable=self.snap_mode, text="Rectangular", value="rect", command=self.redraw)
        self.widget(Radiobutton,side = TOP, anchor = W, variable=self.snap_mode, text="Polar", value="polar", command=self.redraw)
        self.endfr()
        self.fr(LEFT)
        a = self.fr(TOP)
        self.la(LEFT,'both',0,'n',text="Grid Size")
        self.en(LEFT,anchor = N,width=4,textvariable=self.grid_size)
        self.endfr()
        # Again, unsure why the "pack forget/pack" lines ensure that the entry box acts right; without them, it doesn't (it expands fully)
        a.pack_forget()
        a.pack(side=TOP)
        b = self.fr(TOP)
        self.la(LEFT,'both',0,'n',text="Number of Axes")
        self.en(LEFT,anchor = N,width=4,textvariable=self.number_per_circle)
        self.endfr()
        b.pack_forget()
        b.pack(side=TOP)
        self.bu(TOP,text='Update',command=self.redraw)
        self.endfr()
        self.endfr()
        self.endfr()
        self.fr(LEFT, width=2, height=32, bd = 1, bg="grey", expand=0)
        self.endfr()
        self.endfr()
        
        
        self.endfr()
        
        self.fr(LEFT, width=70, expand=0)
        self.subgraph_menu()
        self.endfr()

        self.import_preferences()

    def import_preferences(self):
        if os.path.isfile(os.path.join(os.path.curdir, RELATIVE_PREFERENCE_PATH)):
            pass
        else:
            pass
    
    def help_holes(self):
        helptxt = "Holes Allowed: The generated labelings are simply the smallest labelling; they have no regard for holes.\n\
Holes Minimized: The generated labeling is a labeling with the least number of holes in all samllest-span labelings.\n\
No Holes: The generated labelings contain no holes, at the possible expense of having a larger span."
        tkMessageBox.showinfo("Help!  I need somebody...", helptxt)
        
    def menu_buttons(self,buttons):
        i = 1
        self.regular_buttons=[]
        while i < len(buttons):
            if i != 1: # Draw a grey bar between sections
                self.fr(TOP, width=32, height=5, bd = 4, bg="grey", expand=0)
                self.endfr()        
            self.fr(TOP, width=70, expand=0)
            parity = False
            while i < len(buttons) and type(buttons[i]) != type('str'):
                button = buttons[i]
                if parity == False:
                    self.fr(TOP, expand = 0)
                try:
                    p = PhotoImage(file="icons/" + button['image'])
                    b = self.bu(text=button['name'], image=p, width=32, command=button['command'])
                    b.pack(side=LEFT,padx=2,pady=2)
                    b.image = p
                except:
                    b = self.bu(text=button['name'], width=32, command=button['command'])
                    b.pack(side=LEFT,padx=2,pady=2)
                self.regular_buttons.append(b)
                if parity == True:
                    self.endfr()
                i = i + 1
                parity = not parity
            
            if parity == True:
                self.endfr()
            self.endfr()
            i = i + 1
        
    def subgraph_menu(self):
        self.la(TOP,'both',0,'n',text = 'Insert Subgraph')
        
        subgraphs = []
        subgraphs.append({'name':'petersen', 
                          'command':lambda: self.select_subgraph('petersen'), 
                          'options':[['vertices/layer',6],['layers',2]]})
        subgraphs.append({'name':'cycle',
                          'command':lambda: self.select_subgraph('cycle'),
                          'options':[['vertices/cycle',5],['layers',1]]})
        subgraphs.append({'name':'grid',
                          'command':lambda: self.select_subgraph('grid'),
                          'options':[['rows',5],['columns',4]]})
        subgraphs.append({'name':'star',
                          'command':lambda: self.select_subgraph('star'),
                          'options':[['vertices/cycle',5],['skip',2]]})                  
        subgraphs.append({'name':'mobius',
                          'command':lambda: self.select_subgraph('mobius'),
                          'options':[['n',5]]})
        subgraphs.append({'name':'triangles',
                          'command':lambda: self.select_subgraph('triangles'),
                          'options':[['n',5],['m',5], ['sheet(1),\ncylinder(2),\ntoroid(3)',1]]})
        subgraphs.append({'name':'hexagons',
                          'command':lambda: self.select_subgraph('hexagons'),
                          'options':[['n',5],['m',5], ['sheet(1),\ncylinder(2),\ntoroid(3)',1]]})
        subgraphs.append({'name':'partite',
                          'command':lambda: self.select_subgraph('partite'),
                          'options':[['sizes','3,4,3']]}) 
        subgraphs.append({'name':'file',
                          'command':lambda: self.select_subgraph('file'),
                          'options':[]})
        self.subgraph_buttons = []
        
        parity = False
        self.fr(TOP, width=70, expand=0)
        for subgraph in subgraphs:
            if parity == False:
                self.fr(TOP, expand = 0)
            try:
                p = PhotoImage(file="icons/subgraphs/" + subgraph['name'] + ".gif")
                b = self.bu(text=subgraph['name'], width=64, image=p, command=subgraph['command'])
                b.pack(side=LEFT,padx=2,pady=2)
                b.image = p
            except:
                b=self.bu(text=subgraph['name'], width=64, command=subgraph['command'])
            b.name = subgraph['name']
            b.options = subgraph['options']
            self.subgraph_buttons.append(b)
            if parity == True:
                self.endfr()
            parity = not parity
        if parity == True:
            self.endfr()
        
        self.subgraph_entries = []
        
        for i in range(5):
            this_frame = self.fr(side=TOP, anchor=W)
            # ## NOTE: if the next two lines aren't added, the first box expands full width.  Not sure exactly why...
            this_frame.pack_forget()
            this_frame.pack(side=TOP, anchor=W)
            # ## NOTE: this did not happen for me when I removed them. PB.
            self.subgraph_entries.append((self.la(LEFT,text=""),
                                          self.en(LEFT,width = 4),
                                          this_frame))
            self.endfr()
        
        self.subgraph_button_frame = self.fr(TOP)
        self.bu(text="Insert Subgraph", command=self.insert_subgraph)
        self.endfr()
        
        self.endfr()
        
        
        self.selected_subgraph = None
        self.select_subgraph(subgraphs[0]['name'])
        
    def makemenus(self):
        menu=Menu(self)
        self.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New (ctrl-n)", command=self.new)
        filemenu.add_command(label="Save (ctrl-s)", command=self.saveas)
        filemenu.add_command(label="Save Sequence", command=self.savesequence)
        filemenu.add_command(label="Open (ctrl-o)", command=self.open)
        filemenu.add_command(label="Open sequence", command=self.opensequence)
        filemenu.add_command(label="Print (ctrl-p)", command=self.printcanv)
        filemenu.add_separator()
        filemenu.add_command(label="Import Regular Graph File (first graph)", command=self.import_graph)
        filemenu.add_command(label="Import GPGs", command=self.import_GPGs)
        filemenu.add_command(label="Enter Shortcode", command=self.enter_shortcode)
        filemenu.add_command(label="Enter GPGPermutation", command=self.enter_GPGpermutation)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)

        editmenu = Menu(menu)
        menu.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Cut (ctrl-x)", command=self.cut)
        editmenu.add_command(label="Copy (ctrl-c)", command=self.copy)
        editmenu.add_command(label="Paste (ctrl-v)", command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="Undo (ctrl-z)", command=self.undo)
        editmenu.add_command(label="Redo (ctrl-y)", command=self.redo)

        labelmenu = Menu(menu)
        menu.add_cascade(label="Labeling", menu=labelmenu)
        labelmenu.add_command(label="Label Selected Vertices", command=self.label_message)
        #labelmenu.add_command(label="Label (with reals) Selected Vertices", command=self.label_real_message)
        labelmenu.add_command(label="Unlabel Selected Vertices (ctrl-u)", command=self.unlabel_vertex)
        labelmenu.add_command(label="Clear Labeling", command=self.clear_labeling)
        labelmenu.add_separator()
        labelmenu.add_command(label="Auto-Label/Finish Labeling Graph", command=self.autolabel_message)
        #labelmenu.add_command(label="Find Lambda Number (clears current labeling)", command=self.lambda_label_message)
        labelmenu.add_command(label="Check Labeling", command=self.check_labeling)
        labelmenu.add_command(label="Count Holes", command=self.count_holes)

        graphmenu = Menu(menu)
        menu.add_cascade(label="Graphs", menu=graphmenu)
        graphmenu.add_command(label="Graph Complement", command=self.complement)
        graphmenu.add_command(label="Line Graph", command=self.line_graph)
        graphmenu.add_command(label="Box Everything", command=self.box_all)
        graphmenu.add_separator()
        graphmenu.add_command(label="Process Regular Graph File", command=self.process_regular_graph)
        graphmenu.add_separator()
        graphmenu.add_command(label="Get Graph Representations", command=self.get_graph_representations)
        # graphmenu.add_command(label="Check Isomorphism", command=self.check_isomorphic)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Help (F1)", command=self.helptext)
        helpmenu.add_command(label="About", command=self.abouttext)


    def helptext(self, event=None):
        basics = "Creating Vertices and Edges:\n\
  To create vertices, simply shift-click on an empty spot.\n\
  To create edges, either select multiple vertices, and right click and select 'connect', or...\n\
  Hold down CTRL and click and drag.  Release the mouse, and you will create the edge.  Note that \n\
    none, one, or both of the endpoints may be existing vertices.\n\
\n\
Editing the Edges:\n\
  To wrap edges, first select the edges.  Then either click the 'wrap' button from the left side, or\n\
    right click and select 'wrap'.\n\
  To curve edges, just drag an edge, and it will curve along your cursor (try it!)\n\
  For a different method for curving, first select the edges.  Then either click the 'curve' button from\n\
    the left side, or right click and select 'curve'.\n\
  Note that edges cannot be both curved and wrapped, and curving win take over if both are selected.\n\
\n\
Selecting and Moving:\n\
  Click on an edge or vertex to select it.  Click and drag a vertex to move it.\n\
  Also, there is an 'area select' mode, where you can drag and select everything inside a rectangle.  After\n\
    you make your selection, you can click and drag the entire box, or resize by dragging the handles.\n\
  You can always press 'Escape' to unselect everything, including any area select box.\n\
\n\
Cut, Copy and Paste:\n\
  To cut, copy, or paste, use either the keyboard shortcuts, right click, use the button on the left menu, or select\n\
    from the 'edit' drop down menu.\n\
  After you click to 'paste', you must then click somewhere on the drawing area.  The pasted graph can then be \n\
    or resized via the box methods.\n"
        more_advanced = "Labeling:\n\
  To label, either right click, or select 'label' from the top drop-down menu.\n\
  You can label with either reals or integers using the same dialog.\n\
  Note that real numbers are much slower in solving, due to more complex representation in the computer.\n\
\n\
Physics Mode:\n\
  This can now be started and stopped via the buttons on the left menu or by pressing Ctrl-H.\n\
  Press up and down to control vertex spacing (pushing away from each other) \n\
  and left and right to control attraction along edges\n\
\n\
Key Shortcuts:\n\
  Most key shortcuts are noted in the top drop down menus. For brevity, we only include the others here.\n\
\n\
    Ctrl-A: Select All\n\
    Ctrl-E: Select Edges\n\
    Ctrl-B: Select Vertices\n\
\n\
    Delete: Delete Selected\n\
    Escape: Deselect All\n\
    F1: Help\n\
    Ctrl-<number>: complete L(2,1)-Labeling with minimum lambda <number> or find a k-conversion set with <number> vertices\n\
    Ctrl-F: finish k-conversion with already labeled vertices\n\
    Ctrl-0: step through one step of the k-conversion process\n\
\n\
Right Click:\n\
  You can right click on the drawing area to access commonly used functions from a pop up menu.\n\
\n\
Auto-Update:\n\
  You should always have the latest version!\n\
  Each time the program starts, it tries to connect to the internet, and downloads the latest version of itself.\n\
  This is meant to be very unobtrusive, but a useful way to provide quick updates and bug fixes.\n\
  Although the delay shouldn't be noticeable, it this becomes an issue, there is a simple way to disable it.\n\
    (Note: Is is not recommended to disable this!)\n\
\n\
Easy Install:\n\
  As a side effect of the auto-update, the program is a snap to install.  Just double click on the update file (start.py),\n\
    and the entire program is downloaded to the folder containing start.py.\n"
        
        about_the_menus = "Menus/Parts of the GUI:\n\
  Simple Top Menu\n\
    Key shortcuts are given in the drop down top menus.\n\
\n\
  Buttons on the Left Menu\n\
    File Commands (New, Open, Save, and Print)\n\
    Edit Commands (Undo, Redo, Cut, Copy, and Paste)\n\
    Edge Commands (Curve, Connect, Wrap)\n\
    Physics Commands (Start, Stop)\n\
    Product Commands (Cartesian, Tensor, Strong)\n\
        -make graph, click product button to store first graph. alter or make a new, second graph, press product button to create the product of the first and second graph\n\
\n\
  Insert Subgraph Menu\n\
    You can insert subgraphs without clearing the existing graph.\n\
\n\
  Bottom Bar\n\
    Can change of labeling constraints. (single number - k conversion, list of numbers (2,1 or 1,0) L(n,m) labeling, M - majority conversion)\n\
    Can change hole algorithm.\n\
    Easy setup or change grid for snapping."
        
        tkMessageBox.showinfo("Basic Help (P1/3)", basics)
        tkMessageBox.showinfo("More Advanced Help (P2/3)", more_advanced)
        tkMessageBox.showinfo("An overview of the Menus (P3/3)", about_the_menus)
    
    def abouttext(self, event=None):
        abouttxt = "Olin Graph Program\n\
\n\
Created by Jon Cass, Cody Wheeland, and Matthew Tesch\n\
\n\
Email iamtesch@gmail.com for feature requests, questions, or help."
        tkMessageBox.showinfo("About", abouttxt)

# #####################################################################################################		
# File operations (New, Open, Save, Import, Print, Exit):
# #####################################################################################################

    def new(self, event=None):
        self.querysave()
        if not self.cancelled:
            self.clear()
            self.backups = []
            self.redos = []
        self.cancelled=False
        self.control_up()

    def open(self, event=None):
        #self.querysave()
        if not self.cancelled:
            file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
            if file != None:
                self.backups = []
                self.redos = []
                print file.name
                if (file.name.endswith('txt')):
                    print "okay, text file"
                    self.graph = Graph()
                    print "made default graph. now to load based on matrix"
                    adj = self.readasadjacencymatrix(file)
                    if (adj !=[]):
                        print "Got a matrix! loading as adjacency matrix."
                        self.graph.loadadjmatrix()
                    else:
                        print "hmm no matrix available. Is this GPGnumbers (inner cycle orderings)?"
                        #TODO: PUT NEM CODES FOR READING EACH LINE AND graph.loadGPG(order) each line as a list and store in ctrl-z
                    
                else:
                    self.graph = pickle.load(file)                    
                file.close()
                self.redraw()
        self.cancelled=False
        self.control_up()

    def readasadjacencymatrix(self, file):
        adj = []
        row=-1
        
        c = file.read(1)
        while (c and c != '['):
            print "looking for [:", c
            c = file.read(1)
        c = file.read(1)
        while ( c ):
            print c,
            if (c=='['):
                if (len(adj)>0 and adj[-1]==[]):
                    print "This one is ready!"
                    graph= Graph()
                    graph.loadadjmatrix(adj[:-1])
                    self.redos.append(graph)
                    self.backups.append(graph)
                    row=0
                    adj=[[]]
                else:
                    adj.append([])
                    row+=1
            else:
                if c.isdigit():
                    adj[row].append(int(c))
            c = file.read(1)
        print "\nGot this adj:", adj
        return adj
    
    def opensequence(self, event=None):
        #self.querysave()
        if not self.cancelled:
            file = tkFileDialog.askopenfile(parent=self,mode='rb',filetypes=[('Graph Sequence','*.graphs')],title='Choose a file')
            if file != None:
                self.backups = []
                self.redos = pickle.load(file)
                self.graph = self.redos[len(self.redos)-1]
                file.close()
                self.redraw()
        self.cancelled=False
        self.control_up()
        
    def saveas(self, event=None, fileName=None):
        if not self.cancelled:
            if not fileName:
                fileName = tkFileDialog.asksaveasfilename(parent=self,filetypes=myFormats,title="Save the graph as...")
            if len(fileName ) > 0:
                if ('.' in fileName and '.graph' not in fileName):
##                    try:
                        self.draw_to_file(fileName)
##                    except:
##                        tkMessageBox.showinfo("You need PIL!", "It looks like you don't have PIL.\nYou need the Python Imaging Library to save to an image!\nhttp://www.pythonware.com/products/pil/")
                else:
                    if '.graph' not in fileName:
                        fileName += '.graph'
                    f=file(fileName, 'wb')
                    pickle.dump(self.graph,f)
                    f.close()
        self.cancelled=False
        
        self.control_up()
        
    def savesequence(self, event=None, fileName=None):
        if not self.cancelled:
            if not fileName:
                fileName = tkFileDialog.asksaveasfilename(parent=self,filetypes=[('Graph Sequence','*.graphs')],title="Save the graph sequence as...")
            if len(fileName ) > 0:
                if '.graphs' not in fileName:
                    fileName += '.graphs'
                f=file(fileName, 'wb')
                
                pickle.dump(self.redos,f)
                f.close()
        self.cancelled=False
        
        self.control_up()
    def querysave(self):
        self.message("Save?", "Would you like to save?", self.saveas, "yesnocancel")
        self.control_up()
    def draw_to_file(self, filename):
        width=int(self.canvas.winfo_width())
        height=int(self.canvas.winfo_height())
        image1 = Image.new("RGB", (width, height), (255,255,255))
        draw = ImageDraw.Draw(image1)
        draw=self.graph.draw_to_file(draw,width,height)
        image1.save(filename)
        
    def import_graph(self):
        file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
        if file != None:
            self.clear()
            self.graph = Graph(labelingConstraints=self.graph.labelingConstraints)
            
            if file.name.endswith('.scd'):
                nums=self.readshortcode(file)
                for graph in self.graph.loadshortcode(nums, all=False):
                    self.graph=graph
            else:                
                adjlist = []
                while file:
                    line = file.readline()
                    if line[0:5] == "Graph":
                        line = file.readline()
                        line = file.readline()
                        while line[0:5] != "Taill":
                            line = line.split()
                            line.remove(":")
                            for i in range(len(line)):
                                line[i] = int(line[i])
                            adjlist.append(line)
                            line = file.readline()
                        break
                self.graph.loadadjlist(adjlist)
            file.close()
            self.redraw()
        self.control_up()
        
    def import_GPGs(self):
        file = tkFileDialog.askopenfile(parent=self,mode='r',title='Choose a file')
        if file !=None:
            self.clear()
            numgraphs=sum(1 for line in file)
            file.seek(0)
            graphcounter=0;
            rows=5

            cols=5
            for i in xrange(1,5):
                if i*i>numgraphs:
                    rows=cols=i
                    break
            spacing=20
            canvas_width=self.canvas.winfo_width()
            canvas_height=self.canvas.winfo_height()
            w=(canvas_width-spacing*(cols+1))/cols
            h=(canvas_height-spacing*(rows+1))/rows
            
            for line in file:
                nums=list(line.strip())
                for i in xrange(len(nums)):
                    nums[i]=int(nums[i])
                g=Graph(labelingConstraints=self.graph.labelingConstraints)
                g.loadGPG(nums)
                labels=[]
                verts=g.get_vertices()
                edges=g.edges
                constraints=g.labelingConstraints
                if type(constraints)==type([]):
                    labels = graphmath.auto_label(verts, edges, constraints, 5, self.holes_mode.get())
                else:
                    labels=graphmath.finishklabeling(verts,edges,constraints)
                i=0
                for vert in g.get_vertices():
                    vert.label=labels[i]
                    vert.x*=w/400.
                    vert.y*=h/400.
                    col=graphcounter%cols
                    row=(graphcounter%(rows*cols))/rows
                    x=col*w+w/2+spacing*(col+1)-canvas_width/2
                    y=row*h+h/2+spacing*(row+1)-canvas_height/2
                    vert.x+=x
                    vert.y+=y
                    self.graph.add_vertex(vert)
                    i+=1
                for edge in g.edges:
                    self.graph.edges.append(edge)
                graphcounter+=1
                if graphcounter%(rows*cols)==0:
                    self.saveas(fileName=file.name[:-4]+'-'+str(graphcounter/(rows*cols))+'.png')
                    self.clear()
            self.saveas(fileName=file.name[:-4]+'-'+str(graphcounter/(rows*cols)+1)+'.png')
            file.close()
            self.redraw()
            
    def enter_shortcode(self):
        res = tkSimpleDialog.askstring("Enter Shortcode", "Enter Shortcode to load:")
        res=res.split(',')
        if len(res)==1:
            res=res[0].split()
        if len(res)==1:
            num=int(res[0])
            res=[]
            while num>0:
                res.append(num%10)
                num/=10
        if res[0]=='0':
            del res[0]
        for i in xrange(len(res)):
            res[i]=int(res[i])
        res.insert(0,max(res)) #the number of vertices will be the highest number in the edge-list
        res.insert(1,len(res)*2/res[0])
        res.insert(2,0)
        for graph in self.graph.loadshortcode(res, all=False):
            self.graph=graph
        self.redraw()
        
    def enter_GPGpermutation(self):
        res = tkSimpleDialog.askstring("Enter Permutation", "Enter permutation to load:")

        res=res.split(',')
        if len(res)==1:
            res=res[0].split()
        if len(res)==1:
            num=res
            res=[]
            for i in xrange(len(num)):
                res.append(int(num[i]))
        for i in xrange(len(res)):
            res[i]=int(res[i])
        print res
        self.graph.loadGPG(res)
        self.redraw()
    def process_regular_graph(self):
        infile = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
        outfilename = tkFileDialog.asksaveasfilename(parent=self,title="Save the output as...")
        if len(outfilename) > 0:
            outfile=file(outfilename, 'w')
        else:
            outfile=file('out.txt', 'w')
        self.cancelled=False
        if infile != None:
            # self.holes_mode.set("minimize")   # I really don't think this should be here, or else it resets every time we process.  We want to process with the current settings.
            tempgraph = deepcopy(self.graph)
            self.clear()
            self.graph = Graph(labelingConstraints=self.graph.labelingConstraints) # we want to keep the existing labeling constraints here

            if infile.name.endswith('.scd'):
                nums=self.readshortcode(infile)
                for graph in self.graph.loadshortcode(nums, all=True):
                    self.graph=graph
                    self.clear_labeling()
                    lnum = self.autolabel(0,quiet=True)
                    outfile.write("Lambda: "+str(lnum)+"\r\n")
                    holes = self.count_holes(quiet=True)
                    outfile.write("Holes: "+str(holes)+"\r\n")
            else:                
                line = 'beginning' # some value so the while loop goes at least once...
                while line != '':
                    line = infile.readline()
                    if line[0:5] == "Graph":
                        line = infile.readline()
                        line = infile.readline()
                        adjlist = []
                        while line[0:5] != "Taill":
                            line = line.split()
                            line.remove(":")
                            for i in range(len(line)):
                                line[i] = int(line[i])
                            adjlist.append(line)
                            line = infile.readline()
                        self.graph.loadadjlist(adjlist)
                        self.clear_labeling()
                        lnum = self.autolabel(0,quiet=True)
                        outfile.write("Lambda: "+str(lnum)+"\r\n")
                        holes = self.count_holes(quiet=True)
                        outfile.write("Holes: "+str(holes)+"\r\n")
            self.graph = tempgraph
            infile.close()
            outfile.close()
            self.redraw()
    def get_graph_representations(self):
        adj=graphmath.adjacencymatrix(self.graph.get_vertices(),self.graph.edges)
        adjmessage = "Adjacency Matrix\n---------------------\n"
        try:
            w,v = graphmath.eig(adj)
            adjmessage += "eigenvalues:"+str(w)+" NRG="+str(w.sum()) +"\n" #eigenvalues check
        except:
            print "Warning: No eigenvalue information without numpy module."
        for i in xrange(len(adj)):
            adjmessage+=str(adj[i])+"\n"
        spm=graphmath.shortestpathmatrix(self.graph.get_vertices(),self.graph.edges)
        spmmessage= "Shortest Path Matrix\n------------------------\n"
        for i in xrange(len(spm)):
            spmmessage+=str(spm[i])+"\n"
        d2m=graphmath.adjacencyToDist2Matrix(adj)
        d2mmessage= "Distance 1-2 Matrix:" +"\n------------------------\n"
        for i in xrange(len(d2m)):
            d2mmessage+=str(d2m[i])+"\n"
        scmessage="Shortcode\n------------\n"
        if graphmath.is_regular(self.graph.get_vertices(),self.graph.edges):
            scmessage+=str(graphmath.generate_shortcode(self.graph.get_vertices(),self.graph.edges))
        else:
            scmessage+="The graph is not regular.\nA shortcode doesn't make sense."
        if len(self.graph.get_vertices())<10:
            tkMessageBox.showinfo("Graph Representations:",adjmessage+"\n"+spmmessage+"\n"+d2mmessage+"\n"+scmessage)
        else:
            tkMessageBox.showinfo("Graph Representations (P1/4):",adjmessage)
            tkMessageBox.showinfo("Graph Representations (P2/4):",spmmessage)
            tkMessageBox.showinfo("Graph Representations (P3/4):",d2mmessage)
            tkMessageBox.showinfo("Graph Representations (P4/4):",scmessage)

    #reads a shortcode file, returns list with the numeric elements of the file
    #first two elements are number of vertices and the regularity of the graph
    #shortcode is for k-regular graphs on n-vertices, produced by genreg program
    def readshortcode(self, f, full=True):
        name=os.path.split(f.name)[-1]
        name=name.split('_')
        k=int(name[1])
        n=int(name[0])
        s=f.read(1)
        nums=[n, k]
        while s:
            nums.append(ord(s))
            s=f.read(1)
            if not full and len(nums)==2+n*k/2:
                break
        return nums
    
    def printcanv(self, event=None):
        self.canvas.postscript(file="print.ps")
        os.system("PrFile32.exe /q print.ps")

    def cancel(self):
        self.cancelled=True

    def exit(self):
        self.querysave()
        if not self.cancelled:
            sys.exit(0)
        self.cancelled=False

# #####################################################################################################
# Edit Operations: Undo, Redo, Copy, Paste, Connect, Delete, etc.
# #####################################################################################################

    def curve_selected(self, event=None):
        for edge in self.graph.edges:
            if edge.selected:
                edge.curved = not edge.curved
        self.redraw()

    # def curve_height(self, event):
        # step = 0
        # if event.keysym == "Up":
            # step = 1
        # if event.keysym == "Down":
            # step = -1
        # for edge in self.graph.edges:
            # if edge.selected:
                # if not edge.curved:
                    # edge.curved = True
                # edge.height = edge.height + step
        # self.redraw()

    def wrap_selected(self, event=None):
        for edge in self.graph.edges:
            if edge.selected:
                edge.wrap = not edge.wrap
                edge.curved = False
        self.redraw()
    # Call this function before any operation that you want to be "undone".  It saves the state of the graph at that point.
    # (For example, the start of all clicks, new vertices, deletes, etc.)
    def registerwithundo(self):
        self.redos = []
        self.backups.append(deepcopy(self.graph))
        if len(self.backups)>MAXUNDO:
            self.backups.pop(1)

    def undo(self, event=None):
        if len(self.backups) == 0:
            return
        self.redos.append(deepcopy(self.graph))
        self.graph = self.backups.pop()
        self.redraw()

    def redo(self, event=None):
        if len(self.redos) == 0:
            return
        self.backups.append(deepcopy(self.graph))
        self.graph = self.redos.pop()
        self.redraw()
        
    def selection(self):
        sel = [o for o in self.graph.get_vertices() + self.graph.edges if o.selected]
        if sel == []:
            return None
        return sel

    def select_all(self, event=None):
        self.select_edges(all=True)
        self.select_vertices(all=True)

    def select_edges(self, event=None, all=False):
        self.registerwithundo()
        if all:
            for e in self.graph.edges:
                e.selected=True
        else:
            for v in self.graph.get_vertices():
                v.selected=False
        self.redraw()

    def select_vertices(self, event=None,all=False):
        self.registerwithundo()
        if all:
            for v in self.graph.get_vertices():
                v.selected=True
        else:
            for e in self.graph.edges:
                e.selected=False
        self.redraw()

    def deselect_all(self, event=None):
        self.registerwithundo()
        self.box = None
        self.deselect_edges()
        self.deselect_vertices()
        

    def deselect_edges(self, event=None):
        self.registerwithundo()
        for e in self.graph.edges:
            e.selected=False
        self.redraw()

    def deselect_vertices(self, event=None):
        self.registerwithundo()
        for v in self.graph.get_vertices():
            v.selected=False
        self.redraw()
        
    def invert_selected(self, event=None):
        self.registerwithundo()
        for v in self.graph.get_vertices():
            v.selected=not v.selected
        for e in self.graph.edges:
            e.selected=not e.selected
        self.redraw()


    def rotate_selected_message(self, event=None):
        #rotation matrix
        #R= [cos(theta) -sin(theta); sin(theta) cos(theta)]
        self.message("Rotate Selected Vertices", "What angle would you like to rotate these vertices (degrees)?", self.rotate_selected, type="Decimal")
        self.control_up()

    def rotate_selected(self, rotate):
        rotate=radians(rotate)
        n=0
        cx=0; cy=0
        for v in self.graph.get_vertices():
            if v.selected:
                cx+=v.x
                cy+=v.y
                n+=1
        if n != 0:
            cx/=n
            cy/=n
        for v in self.graph.get_vertices():
            if v.selected:
                x = v.x-cx
                y = v.y-cy
                v.x = x * math.cos(rotate) - y * math.sin(rotate) + cx
                v.y = x * math.sin(rotate) + y * math.cos(rotate) + cy
    # Deprecated and unneeded.  Delete this function?
    # def delete_selected_vertices(self, event=None):
        # self.registerwithundo()
        # vr = []
        # for v in self.graph.get_vertices():
            # if v.selected:
                # vr.append(v)
        # for e in self.graph.edges:
            # if v in e.vs:
                # er.append(e)
        # for e in er:
            # try:
                # self.graph.edges.remove(e)
            # except:
                # pass
        # for v in vr:
            # try:
                # self.graph.remove_vertex(v)
            # except:
                # pass
        # self.redraw()
        
    def delete_selected(self, event=None):
        self.registerwithundo()
        er = []
        vr = []
        for e in self.graph.edges:
            if e.selected:
                er.append(e)
        for v in self.graph.get_vertices():
            if v.selected:
                vr.append(v)
                for e in self.graph.edges:
                    if v in e.vs:
                        er.append(e)
        for e in er:
            try:
                self.graph.edges.remove(e)
            except:
                pass
        for v in vr:
            try:
                self.graph.remove_vertex(v)
            except:
                pass
        self.box = False
        self.redraw()        
        
    def connect(self, event=None):
        self.registerwithundo()
        self.graph.connect()
        self.redraw()
        
    def copy(self, event=None, delete=False):
        selectedverts = [v for v in self.graph.get_vertices() if v.selected]
        self.copied_verts = []
        self.copied_edges = []
        for v in selectedverts:
            self.copied_verts.append((v.x,v.y,v.label))
        for e in self.graph.edges:
            if e.vs[0] in selectedverts and e.vs[1] in selectedverts and e.selected:
                self.copied_edges.append(((e.vs[0].x,e.vs[0].y),(e.vs[1].x,e.vs[1].y),[e.wrap,e.curved,e.height,e.direction]))
        if delete==True:
            self.delete_selected()
        else:
            self.deselect_all()
            
    def cut(self, event=None):
        self.registerwithundo()
        self.copy(event=event, delete=True)
        
    def paste(self, event=None):
        self.registerwithundo()
        self.pasting = True
        
    def shift_down(self, event=None):
        self.shift_pressed=True
    def shift_up(self, event=None):
        self.shift_pressed=False

    def choose_color(self):
        self.registerwithundo()
        vert_selected=False
        if len([v for v in self.graph.get_vertices() if v.selected])>0:
            color=tkColorChooser.askcolor(color=self.graph.get_vertices()[0].color,title="Choose a Vertex Color")[1]
            for v in [v for v in self.graph.get_vertices() if v.selected]:
                if color!=None:
                    v.color=color
                if v.label!="NULL":
                    vert_selected=True
            self.redraw();
        if len([edge for edge in self.graph.edges if edge.selected])>0:
            color=tkColorChooser.askcolor(color=self.graph.edges[0].color,title="Choose an Edge Color")[1]
            for edge in [edge for edge in self.graph.edges if edge.selected]:
                edge.color=color
            self.redraw();
        if vert_selected:
            color=tkColorChooser.askcolor(color=self.graph.get_vertices()[0].lcolor,title="Label Color")[1]
            if color!=None:
                for v in [v for v in self.graph.get_vertices() if v.selected]:
                    v.lcolor=color
        self.redraw()


    def pick_size(self, event=None):
        vert_selected=False
        if len([v for v in self.graph.get_vertices() if v.selected])>0:
            size=int(tkSimpleDialog.askstring("Pick Size", "What's a good size for the selected vertices?"))
            if size!=None:
                size=int(size)
                for v in [v for v in self.graph.get_vertices() if v.selected]:
                    if size!=None:
                        v.size=size
                    if v.label!="NULL":
                        vert_selected=True
                self.redraw();
        if len([edge for edge in self.graph.edges if edge.selected])>0:
            size=tkSimpleDialog.askstring("Pick Size", "What's a good width for the selected edges?")
            if size!=None:
                size=int(size)
                for edge in [edge for edge in self.graph.edges if edge.selected]:
                    edge.size=size
                self.redraw();
        if vert_selected:
            size=tkSimpleDialog.askstring("Pick Size", "What's a good width for the labels?")
            if size!=None:
                size=int(size)
                for v in [v for v in self.graph.get_vertices() if v.selected]:
                    v.lsize=size
                self.redraw()

    def select_shape(self, event=None):
        shape=-1
        for v in [v for v in self.graph.get_vertices() if v.selected]:
            if shape==-1:
                if type(v.shape)==type('A'):
                    shape=0
                elif v.shape==8:
                    names=['Harold','Luke','Connor','Paul','Zachary','Dr. Adams','Dr. Troxell']
                    shape=random.choice(names)
                else:
                    shape=(v.shape+1)
                    if shape==7:
                        shape+=1
            v.shape=shape
        
        self.redraw()
        
# #####################################################################################################
# Whole Graph Commands: Complement, Line Graph, etc.  Anything that changes/affects the current graph.  (In the spirit of complement, etc, but not "add new subgraph")
# #####################################################################################################

    def complement(self):
        self.registerwithundo()
        comp = Graph()
        vertices = self.graph.get_vertices()
        comp.vertices = vertices
        comp.edges = []
        for v1 in vertices:
            for v2 in vertices:
                if v1 != v2:
                    found = 0
                    for e in self.graph.edges:
                        if v1 in e.vs and v2 in e.vs:
                            found = 1
                            break
                    if not found:
                        comp.edges.append(Edge(v1,v2))
                        self.graph.edges.append(Edge(v1,v2))
        self.graph = comp
        self.redraw()

    def line_graph(self):
        self.registerwithundo()
        lg = Graph(edges = [])
        i = 0
        lgverts = []
        for e1 in self.graph.edges:
            v = Vertex((.5*e1.vs[0].x+.5*e1.vs[1].x, .5*e1.vs[0].y+.5*e1.vs[1].y))
            lgverts.append(v)
            lg.add_vertex(v)
            for j in range(i):
                e2 = self.graph.edges[j]
                if e1 != e2:
                    if (e1.vs[0] in e2.vs) or (e1.vs[1] in e2.vs):
                        lg.edges.append(Edge(lgverts[i],lgverts[j]))
            i = i + 1
        self.graph = lg
        self.redraw()
# #####################################################################################################
# Product Commands: Commands to create products of graphs
# #####################################################################################################
    def graph_product(self, type, event=None):
        self.registerwithundo()
        if (len(self.product_verts)!=0):
            product_adj=graphmath.adjacencymatrix(self.product_verts,self.product_edges)
            verts = self.graph.get_vertices()
            edges = self.graph.edges
            product_adj2=graphmath.adjacencymatrix(verts,edges)
            adjmat=[]
            if (type=='cartesian'):
                adjmat=graphmath.cartesian_product(product_adj,product_adj2)
            elif(type=='tensor'):
                adjmat=graphmath.tensor_product(product_adj,product_adj2)
            elif(type=='strong'):
                adjmat=graphmath.strong_product(product_adj,product_adj2)
            else:
                print "uh oh. that not a graph product type."
                adjmat=graphmath.cartesian_product(product_adj,product_adj2)
            self.graph = Graph(labelingConstraints =self.graph.labelingConstraints)
            self.graph.loadadjmatrix(adjmat,len(self.product_verts), len(verts),self.product_verts, verts )
            self.product_verts=[]
            self.product_edges=[]
        else:
            self.product_verts=self.graph.get_vertices()[:]
            self.product_edges=self.graph.edges[:]
        self.redraw()
    
# #####################################################################################################
# Labeling Commands: Commands to label, change labeling constraints, etc.
# #####################################################################################################		

    def autolabel_easy(self, event=None):
        if type(self.graph.labelingConstraints)==type([]):
            if self.check_to_clear():
                print "WARNING:clearing labels for autolabeling."
                self.clear_labeling()
            self.autolabel(int(event.keysym))
        else:
            if int(event.keysym)!=0:
                self.autolabel(int(event.keysym))
            else:
                #print "decide which stepthrough"
                #print self.kpath
                if (self.kpath):
                    self.stepthroughkpath()
                else:
                    self.stepthrough()
        self.control_up()

    def check_to_clear(self):
        for vertex in self.graph.vertices:
            if vertex.label == 'NULL':
                return False
        self.control_up()
        return True
            
    # def label_message(self, event=None):
        # self.message("Label Vertices", "What would you like to label these vertices?", self.label_vertex)

    # Note: label_message now takes care of real and integers; integers are transformed to int type in label_vertex.
    def label_message(self, event=None):
        self.message("Label Vertices", "What would you like to label these vertices?", self.label_vertex, type="Decimal")
        self.control_up()

    def autolabel_message(self):
        self.message("Auto-Label Graph", "What is the minimum lambda-number for this graph?", self.autolabel)
        self.control_up()
    # def lambda_label_message(self):
        # self.clear_labeling()
        # self.holes_mode.set("allow")
        # lnum = self.autolabel(0,quiet=True)
        # labeltxt = ""
        # for labConst in self.graph.labelingConstraints:
            # labeltxt += str(labConst) + ","
        # labeltxt = labeltxt[:-1]
        # tkMessageBox.showinfo("Labeling Span", "The L(" + labeltxt + ") lambda number for this graph is " + str(lnum) + ".")

    def constraints_message(self):
        res = ''
        while res == '':
            res = tkSimpleDialog.askstring("Change Labeling Constraints", \
                                           "Please enter new labeling constraints.\n" \
                                            +"Enter a single value for K conversion ('3' for K3).\n" \
                                            +"M - majority, MS - strong majority.\n" \
                                            +"comma deliminated list of values for L(m,n,...) labeling ('2,1' for L(2,1) labeling)")
        self.change_constraints(res)
        self.control_up()

    def change_constraints(self, newconstraints):
        backup = self.graph.labelingConstraints
        if (len(newconstraints)>1 and newconstraints[0].isdigit()):
            self.graph.labelingConstraints = []
            try:
                for label in newconstraints.split(','):
                    label = Decimal(label)
                    if label == int(label):
                        self.graph.labelingConstraints.append(int(label))
                    else:
                        self.graph.labelingConstraints.append(label)
            except:
                tkMessageBox.showinfo("Error", "The labeling constraints were input in a bad form! Using old constraints.")
                self.graph.labelingConstraints = backup
            labeltxt = "Labeling Constraints:\nL("
            for labConst in self.graph.labelingConstraints:
                labeltxt += str(labConst) + ","
            labeltxt = labeltxt[:-1]
            labeltxt += ")"
            self.constraintstxt.set(labeltxt)

        else:            
            self.graph.labelingConstraints = 0
            try:
                label=int(newconstraints[0])
                self.graph.labelingConstraints=label
                labeltxt = "Labeling Constraints:\nK"+ str(label)
            except:
		self.kpath = False
                if newconstraints.upper()[0]=='M':
                    if (len(newconstraints)>1 and newconstraints.upper()[1]=='S'):
                        self.graph.labelingConstraints=-2
                        labeltxt = "Labeling Constraints:\nStrong Majority"
                    else:
                        self.graph.labelingConstraints=-1
                        labeltxt = "Labeling Constraints:\nMajority"
                elif newconstraints.upper()[0] == 'K':
					self.kpath = True
					label = int(newconstraints[1])
					self.graph.labelingConstraints = label
					labeltxt = "Labeling Constraints:\nK-path(" + str(label) +")"
                elif newconstraints.upper()[0] == 'T':
                    labeltxt = "Labeling Constraints:\nTemporary conversion"
                    self.graph.labelingConstraints = -4
                    if newconstraints.upper()[1] == 'M':
                        self.graph.permanentChange = .5
                        self.graph.temporaryChange = .1
                    #Looks like we have a (T)emporary conversion
                    else:
                        
                        self.graph.permanentChange = 4
                        self.graph.temporaryChange = 3
                    #syntax is T 
                else:
                    tkMessageBox.showinfo("Error", "The labeling constraints were input in a bad form! Using old constraints.")
                    self.graph.labelingConstraints = backup
            self.constraintstxt.set(labeltxt)
        self.control_up()
        #print self.kpath
        
    def label_vertex(self, label):            
        self.registerwithundo()
        if int(label) == label:
            label = int(label)
        for v in [v for v in self.graph.get_vertices() if v.selected]:
            v.label=label
        self.redraw()

    def unlabel_vertex(self, event=None):
        self.registerwithundo()
        for v in [v for v in self.graph.get_vertices() if v.selected]:
            v.label='NULL'
        self.redraw()

    def clear_labeling(self, event=None):
        self.registerwithundo()
        for v in self.graph.get_vertices():
            v.label='NULL'
        self.redraw()

    def autolabel(self, minlambda, quiet = False):
        self.registerwithundo()
        print "\nautolabel\n"
        verts = self.graph.get_vertices()
        print "graphgui labels: ", [vert.label for vert in verts]
        edges = self.graph.edges
        constraints = self.graph.labelingConstraints
        labels=[]
        #print "autolabel"
        if type(constraints)==type([]):
            labels = graphmath.auto_label(verts, edges, constraints, minlambda, self.holes_mode.get())
            print "graphgui got labels: ", labels
        else:
            if self.kpath:
                for i in xrange(minlambda):
                    self.stepthroughkpath();
            else:
                if minlambda==-1:
                    print "finishing k-labeling."
                    labels=graphmath.finishklabeling(verts,edges,constraints)
                else:
                    print "finding a conversion set"
                    labels=graphmath.find_conversion_set(verts,edges,constraints, minlambda)
            ##put the control-2-3-4-5-etc code call here
        if labels == "RealError":
            tkMessageBox.showinfo("Holes and Reals don't mix!", "Don't select 'minimize' or 'no holes' with real labels or constraints; this doesn't make sense!")
            self.control_up()
            return
        if labels == False:
            if type(self.graph.labelingConstraints)==type([]):
                tkMessageBox.showinfo("Bad Partial Labeling", "The partial labeling is incorrect.  Please correct before auto-finishing the labeling.")
            else:
                tkMessageBox.showinfo("No conversion set of size " + minlambda,
                                      "There is no conversion set of size " + minlambda + ". If you want, you can try again with a larger size, which will be slower.")
            self.control_up()
            return
        for i in range(len(verts)):
            verts[i].label = labels[i]
        (lmin,lmax,complete)=graphmath.labeling_difference(verts)
        self.redraw()
        lnum = lmax - lmin
        if (not quiet):
            self.control_up()
            if type(self.graph.labelingConstraints)==type([]):
                tkMessageBox.showinfo("Labeling Span", "The labeling span for this coloring is " + str(lnum) + ".\n  Largest label: " + str(lmax) + "\n Smallest label: " + str(lmin))
            elif (minlambda == -1):
                s='The graph is completely covered!'
                if not complete:
                    s='The graph is NOT completely covered.'
                tkMessageBox.showinfo("Conversion Time", "The conversion time for this coloring is " + str(lnum) + ".\n  Largest time: " + str(lmax) + "\n Smallest time: " + str(lmin)+"\n"+s)
        #print "\nautolabel done.\n"
        return lnum

    def check_labeling(self,quiet = False):
        #print "check labeling"
        verts = self.graph.get_vertices()
        edges = self.graph.edges
        constraints = self.graph.labelingConstraints
        res = graphmath.check_labeling(verts,edges,constraints)
        if res == True:
            if not quiet:
                self.control_up()
                tkMessageBox.showinfo("Correct Labeling", "The labeling is correct.")
            return True
        else:  # res is (False,(i,j)), where 'i' and 'j' are the bad vertices
            if not quiet:
                self.control_up()
                self.deselect_vertices()
                verts[res[1][0]].selected = True
                verts[res[1][1]].selected = True
                tkMessageBox.showwarning("Bad labeling", "The selected vertices appears to be wrong.")
                self.redraw()
            return False

    #shouldn't work with real labelings!  TODO: check this! (doesn't break, but shouldn't let you)
    def count_holes(self,quiet = False):
        verts = self.graph.get_vertices()
        lmax = 0
        for v in verts:
            if v.label > lmax:
                lmax = v.label
        numholes = 0
        for i in range(lmax):
            found = 0
            for v in verts:
                if v.label == i:
                    found = 1
                    break
            if not found:
                numholes += 1
        if not quiet:
            self.control_up()
            tkMessageBox.showinfo("Number of Holes", "The number of holes in this labeling is " + str(numholes) + ".")
        return numholes

    def easy_label(self, event=None):
        self.physics_type=int(event.keysym)
        self.temperature+=5

        self.label_vertex(int(event.keysym))
        
    #stepthrough one step in k conversion process
    def stepthrough(self):
	if (self.kpath):
		return self.stepthroughkpath()
        #print "step through"
        verts=self.graph.get_vertices()
        changelist=graphmath.stepthrough(verts,graphmath.adjacencymatrix(verts,self.graph.edges), self.graph.labelingConstraints)
        if len(changelist)!=0:
            self.registerwithundo()
            (lmin,lmax, complete)=graphmath.labeling_difference(verts)
            for vertnum in changelist:
                verts[vertnum].label=lmax+1
            return complete
        else:
            return True

	#stepthrough one step in k path process
    def stepthroughkpath(self):
        #print "step through kpath"
        verts=self.graph.get_vertices()
        changelist=graphmath.stepthroughkpath(verts,graphmath.adjacencymatrix(verts,self.graph.edges), self.graph.labelingConstraints)
        #print changelist
        if len(changelist)!=0:
            self.registerwithundo()
            for vertnum1, vertnum2 in changelist:
                self.graph.edges.append(Edge(verts[vertnum1], verts[vertnum2]))
            return False
        else:
            return True

    def finishklabeling(self,event=None):
        if type(self.graph.labelingConstraints)!=type([]):
            self.autolabel(-1)
# #####################################################################################################
# Gui Bindings: Mouse controlled-commands and helper functions
# #####################################################################################################				

    def find_clicked_on(self, event):
    #TODO: ensure this returns a vertex or edge, not a selection circle or something!
#        for v in self.graph.get_vertices():
#                if x+10 > v.x > x-10 and y+10 > v.y > y-10:
#                    return v

        #TODO:  how about just finding anthing in "self.canvas.find_overlapping"???

        self.closest=self.canvas.find_closest(event.x, event.y)
        try:
            self.closest=self.closest[0]
        except:
            return None
        
        if self.closest in self.canvas.find_overlapping(event.x-10, event.y-10, event.x+10, event.y+10):
            for h in self.handles.keys():
                if self.closest == h:
                    return h
            for v in self.graph.get_vertices():
                if self.closest == v.circle:
                    return v
                if self.shift_pressed and self.closest==v.text:
                    return v
            for e in self.graph.edges:
                if self.closest == e.line or (e.wrap and self.closest == e.altline):
                    return e
                    
        return None
    
    def right_clicked(self, e):

   #     def rClick_Copy(e, apnd=0):
            #e.widget.event_generate('<Control-c>')
   #         print "copy"

        #event.widget.focus()

        nclst=[
            ('Connect Selected', self.connect),
            ('----', None),
            ('Cut', self.cut),
            ('Copy', self.copy),
            ('Paste', self.paste),
            ('----', None),
            ('Label Selected', self.label_message),
            ('Unlabel Selected', self.unlabel_vertex),
            ('----', None),
            ('Wrap Edges', self.wrap_selected),
            ('Curve Edges', self.curve_selected),
            ('----', None),
            ('Change Cursor', self.change_cursor)
            #('Copy', lambda e=e: rClick_Copy(e)),
            #('Paste', lambda e=e: rClick_Paste(e)),
            ]

        rmenu = Menu(None, tearoff=0, takefocus=0)
        # cas = {}
        # cascade = 0

        for (txt, cmd) in nclst:
            if txt == "----":
                rmenu.add_separator()
            else:
                rmenu.add_command(label=txt, command=cmd)
            # if txt.startswith('>>>>>>') or cascade:
                # if txt.startswith('>>>>>>') and cascade and cmd == None:
                    # #done cascade
                    # cascade = 0
                    # rmenu.add_cascade( label=icmd, menu = cas[icmd] )

                # elif cascade:
                    # if txt == ' ------ ':
                        # cas[icmd].add_separator()
                        
                    # else: cas[icmd].add_command(label=txt, command=cmd)

                # else:  # start cascade
                    # cascade = 1
                    # icmd = cmd[:]
                    # cas[icmd] = Tk.Menu(rmenu, tearoff=0, takefocus=0)
            # else:
                # if txt == ' ------ ':
                    # rmenu.add_separator()
                # else: rmenu.add_command(label=txt, command=cmd)

        #rmenu.entryconfigure(0, label = "redemo", state = 'disabled')
        rmenu.tk_popup(e.x_root+10, e.y_root+10,entry="0")

        return "break"
    
    def clicked(self, event):
        #TODO: create "clicked flags" instead of individual variables?
        self.registerwithundo()
        self.clicked_time = time.time()
        self.clicked_pos = (event.x, event.y)
        self.dragging = False
        self.clicked_on = self.find_clicked_on(event)
        self.clicked_create_edge = self.control_pressed
        self.clicked_in_box = False
        self.resize = None
        if self.box:
            center = self.get_center()
            b0 = self.box[0]+center[0]
            b1 = self.box[1]+center[1]
            b2 = self.box[2]+center[0]
            b3 = self.box[3]+center[1]
            xcoords = (b0,b2)
            ycoords = (b1,b3)
            if self.clicked_on in self.handles.keys():
                self.resize = ['m','m']
                if self.handles[self.clicked_on][0] == b0:
                    self.resize[0] = 'l'
                elif self.handles[self.clicked_on][0] == b2:
                    self.resize[0] = 'r'
                if self.handles[self.clicked_on][1] == b1:
                    self.resize[1] = 'l'
                elif self.handles[self.clicked_on][1] == b3:
                    self.resize[1] = 'r'
                center = self.get_center()
                for v in self.surrounded_vertices:
                    try:
                        #v.xnorm = (v.x-self.box[0]+center[0])/(self.box[2]-self.box[0])
                        v.xnorm = (v.x-self.box[0])/(self.box[2]-self.box[0])
                    except:
                        v.xnorm = 0
                    try:
                        #v.ynorm = (v.y-self.box[1]+center[1])/(self.box[3]-self.box[1])
                        v.ynorm = (v.y-self.box[1])/(self.box[3]-self.box[1])
                    except:
                        v.ynorm = 0
            elif min(xcoords) < event.x < max(xcoords) and min(ycoords) < event.y < max(ycoords):
                self.clicked_in_box = (event.x, event.y)
            else:
                self.box = False
        #self.redraw()
                    
        # if self.click_mode == "path":
            # oldtime = self.clickedtime

            # self.clickedtime = time.time()
            # if self.clickedtime-oldtime < .25:  # Double click!
                # self.graph.lastvertex = None
                # return

            # single click...
            # v = None
            # for vert in self.graph.get_vertices():
                # if x+10 > vert.x > x-10 and y+10 > vert.y > y-10:
                    # v = vert
                    # break
            # if v == None:
                # v = Vertex((x, y))
                # self.graph.add_vertex(v)
            # if self.graph.lastvertex != None:
                # self.graph.connect((v, self.graph.lastvertex))
            # self.graph.lastvertex = v
            # self.redraw()

    def move_box(self, event):
        dx = event.x - self.clicked_in_box[0]
        dy = event.y - self.clicked_in_box[1]
        for v in self.surrounded_vertices:
            v.x += dx
            v.y += dy
        self.box[0] += dx
        self.box[1] += dy
        self.box[2] += dx
        self.box[3] += dy
        self.clicked_in_box = (event.x, event.y)
        
    def resize_box(self, event):
        center = self.get_center()
        if self.resize[0] == 'l':
            self.box[0] = event.x - center[0]
        elif self.resize[0] == 'r':
            self.box[2] = event.x - center[0]
        if self.resize[1] == 'l':
            self.box[1] = event.y - center[1]
        elif self.resize[1] == 'r':
            self.box[3] = event.y - center[1]
        
        for v in self.surrounded_vertices:
            v.x = v.xnorm*(self.box[2]-self.box[0])+self.box[0]
            v.y = v.ynorm*(self.box[3]-self.box[1])+self.box[1]

            
    def dragged(self, event):
        center = self.get_center()
        x = event.x - center[0]
        y = event.y - center[1]
        if self.dragging or (time.time() - self.clicked_time > .15):
            self.dragging = True            
            if self.clicked_create_edge:
                if self.control_pressed:
                    try:
                        self.canvas.delete(self.drag_shape)
                    except:
                        pass
                    self.drag_shape = self.canvas.create_line(self.clicked_pos[0], self.clicked_pos[1], event.x, event.y, width=4, fill="blue")
                return
            elif self.box:
                if self.resize:
                    self.resize_box(event)
                if self.clicked_in_box:
                    self.move_box(event)
                self.redraw()
            else: #no box
                if self.clicked_on in self.graph.edges: # If we clicked on an edge
                    #do "drag-curving" logic/trig here.
                    self.clicked_on.curve_through(x,y)
                    self.redraw()
                elif self.clicked_on in self.graph.get_vertices(): #If we clicked and dragged a vertex...
                    if self.shift_pressed:
                      self.clicked_on.lx=x-self.clicked_on.x
                      self.clicked_on.ly=y-self.clicked_on.y
                    elif self.snap_mode.get() != 'none': #snap-move vertex
                        self.snap(event, self.clicked_on)
                    else: #move vertex
                        self.clicked_on.x = x
                        self.clicked_on.y = y
                    self.redraw()
                else: #if we are drag-selecting
                    try:
                        self.canvas.delete(self.drag_shape)
                    except:
                        pass
                    self.drag_shape = self.canvas.create_rectangle(self.clicked_pos[0], self.clicked_pos[1], event.x, event.y, width=2, outline="blue", tags="bounding box")
                
               
                # elif self.clickedon in self.graph.get_vertices():
                    # if self.drag_mode == "single" or self.drag_mode == "selected":
                        # if self.snap_on:
                            # dx = event.x - self.clickedon.x
                            # dy = event.y - self.clickedon.y
                            # 
                        # else:
                            # dx = x - self.clickedon.x
                            # dy = y - self.clickedon.y
                        # self.redraw()
                    # if self.drag_mode == "selected":
                        # for v in self.graph.get_vertices():
                            # if v.selected and v != self.clickedon:
                                # if self.snap_on:
                                    # e = FakeEvent(v.x + dx,v.y + dy)
                                    # self.snap(e, v)
                                # else:
                                    # v.x += dx
                                    # v.y += dy

                # self.redraw()

    def released(self, event):
        center = self.get_center()
        x = event.x - center[0]
        y = event.y - center[1]
        
        if self.dragging: #We've been dragging.
            if self.clicked_create_edge:
                if self.control_pressed:
                    self.drag_to_create_edge(event) # create Edge
            elif self.box:
                pass #we've already done these steps in the "dragged" function...
            else: #no box
                if self.clicked_on in self.graph.edges: # If we clicked on an edge
                    pass
                    #do "drag-curving" logic/trig here.
                    #self. curve_through(edge, point)
                elif self.clicked_on in self.graph.get_vertices(): #If we clicked and dragged a vertex...
                    pass #we've already moved it in the "dragged" function -- nothing more to do here!
                else: #if we are drag-selecting
                    xcoords = [event.x,self.clicked_pos[0]]
                    ycoords = [event.y,self.clicked_pos[1]]
                    self.surrounded_vertices = []
                    for v in self.graph.get_vertices():
                        if min(xcoords) < v.x + center[0] < max(xcoords) and min(ycoords) < v.y + center[1] < max(ycoords):
                            self.surrounded_vertices.append(v)
                            v.selected = True
                    for e in self.graph.edges:
                        if e.vs[0] in self.surrounded_vertices and e.vs[1] in self.surrounded_vertices:
                            e.selected = True
                    self.box = [self.clicked_pos[0]-center[0],self.clicked_pos[1]-center[1],event.x-center[0],event.y-center[1]]

        else: #We're not draggin!
            if self.pasting: #if pasting/insert subgraph is true:
                self.insert_copied(event)
                self.pasting = False
                #insert subgraph
            elif self.clicked_on in self.graph.get_vertices() or self.clicked_on in self.graph.edges: # If we clicked on something
                #Toggle its selection
                self.clicked_on.toggle()
                self.clicked_on.draw(self.canvas)
            elif (self.selection() != None or self.box) and not self.shift_pressed: #elif something is selected (and clicked on nothing) and not pressing shift
                self.deselect_all()
            elif(self.shift_pressed): # If we clicked on nothing, and nothing is selected or pressing shift (to make a new vertex)
                newVertex = Vertex((x, y))
                if self.snap_mode.get() != 'none':
                    self.snap( event, newVertex )
                self.graph.add_vertex( newVertex )
        self.redraw()
        
    def change_cursor(self, event=None):
        self.config(cursor=random.choice(['bottom_tee', 'heart', 'double_arrow', 'top_left_arrow',
                                          'top_side', 'top_left_corner', 'X_cursor', 'dotbox',
                                          'lr_angle', 'sb_down_arrow', 'draft_small', 'gumby',
                                          'bottom_right_corner', 'hand2', 'sb_right_arrow', 'diamond_cross',
                                          'umbrella', 'mouse', 'trek', 'bottom_side', 'spraycan', 'll_angle',
                                          'based_arrow_down', 'rightbutton', 'clock', 'right_ptr', 'sailboat', 'draft_large',
                                          'cross', 'fleur', 'left_tee', 'boat', 'sb_left_arrow', 'shuttle', 'plus', 'bogosity',
                                          'man', 'pirate', 'bottom_left_corner', 'pencil', 'star', 'arrow', 'exchange', 'gobbler',
                                          'iron_cross', 'left_side', 'xterm', 'watch', 'leftbutton', 'spider', 'sizing', 'ul_angle',
                                          'center_ptr', 'circle', 'icon', 'sb_up_arrow', 'draped_box', 'box_spiral', 'rtl_logo',
                                          'target', 'middlebutton', 'question_arrow', 'cross_reverse', 'sb_v_double_arrow', 'right_side',
                                          'top_right_corner', 'top_tee', 'ur_angle', 'sb_h_double_arrow', 'left_ptr', 'crosshair',
                                          'coffee_mug', 'right_tee', 'based_arrow_up', 'tcross', 'dot', 'hand1']))

    def insert_copied(self, event):
        center = self.get_center()
        x = event.x - center[0]
        y = event.y - center[1]
        
        vertdict = {}
        leastx = 100000
        mostx = -100000
        leasty = 100000
        mosty = -100000
        for v in self.copied_verts:
            if v[0] > mostx:
                mostx = v[0]
            if v[1] > mosty:
                mosty = v[1]
            if v[0] < leastx:
                leastx = v[0]
            if v[1] < leasty:
                leasty = v[1]
        avgx = (mostx + leastx) / 2
        avgy = (mosty + leasty) / 2
        self.deselect_all()
        for v in self.copied_verts:
            # In case we insert a graph with labels undefined
            if len(v) < 3:
                v = (v[0], v[1], "NULL")
            vertdict[(v[0],v[1])] = Vertex((x+v[0]-avgx,y+v[1]-avgy),v[2])
            self.graph.add_vertex( vertdict[(v[0],v[1])] )
        for e in self.copied_edges:
            if len(e) < 3:
            # In case we insert a graph with edge curviness/wrapped-ness undefined
                e = (e[0], e[1], None)
            self.graph.connect((vertdict[e[0]],vertdict[e[1]]),e[2])
        for v in vertdict.values():
            v.toggle()
        for e in self.graph.edges:
            if e.vs[0] in vertdict.values() and e.vs[1] in vertdict.values():
                e.toggle()
        self.surrounded_vertices = vertdict.values()
        
        self.box = [x-(mostx-leastx)/2, y-(mosty-leasty)/2, x+(mostx-leastx)/2, y+(mosty-leasty)/2]
        
    def box_none(self,event=None):
        self.box=False
        self.surrounded_vertices=[]
        self.redraw()

    def box_all(self,event=None):
        leastx = 100000
        mostx = -100000
        leasty = 100000
        mosty = -100000
        for v in self.graph.get_vertices():
            if v.x > mostx:
                mostx = v.x
            if v.y > mosty:
                mosty = v.y
            if v.x < leastx:
                leastx = v.x
            if v.y < leasty:
                leasty = v.y
        self.box = [leastx-10,  leasty-10,mostx+10, mosty+10]
        self.surrounded_vertices=[v for v in self.graph.get_vertices()]
        self.select_all()
        
    def drag_to_create_edge(self, event):
        center = self.get_center()
        x = event.x - center[0]
        y = event.y - center[1]
        
        if self.clicked_on in self.graph.get_vertices():
            v1 = self.clicked_on
        else:
            v1 = Vertex((self.clicked_pos[0]-center[0], self.clicked_pos[1]-center[1]))
            if self.snap_mode.get() != 'none':
                self.snap(FakeEvent(self.clicked_pos[0], self.clicked_pos[1]), v1)
            self.graph.add_vertex(v1)
        self.redraw()
        released_on = self.find_clicked_on(event)
        if released_on in self.graph.get_vertices():
            v2 = released_on
        else:
            v2 = Vertex((x, y))
            if self.snap_mode.get() != 'none':
                self.snap(event, v2)
            self.graph.add_vertex(v2)
        self.graph.connect(vs = (v1,v2))        

# #####################################################################################################
# Other Functions
# #####################################################################################################				

    def do_physics(self):
        spacing = self.spacing
        attraction = self.attraction
        vertices = self.graph.get_vertices()
        vertices2 = vertices[:]
        #print self.physics_type,
        if (self.physics_type ==0):
            for i in xrange(len(vertices)):
                vertex=vertices2[random.randrange(0,len(vertices2))]
                vertices2.remove(vertex)
                for vertex2 in vertices2:
                    x_distance = vertex.x - vertex2.x
                    y_distance = vertex.y - vertex2.y
                    distance2 = (x_distance * x_distance) +  (y_distance * y_distance)
                    if  (vertex.x != vertex2.x or vertex.y != vertex2.y) and (distance2 < 10000 ):
                        if x_distance != 0:
                            delta_x = x_distance * spacing / distance2
                            if not vertex.selected:
                                vertex.x = vertex.x + delta_x
                            if not vertex2.selected:
                                vertex2.x = vertex2.x - delta_x
                        if y_distance != 0:
                            delta_y = y_distance * spacing / distance2
                            if not vertex.selected:
                                vertex.y = vertex.y + delta_y
                            if not vertex2.selected:
                                vertex2.y = vertex2.y - delta_y
            for edge in self.graph.edges:
                vertices = edge.vs
                distance = math.sqrt( math.pow( vertices[0].x - vertices[1].x, 2 ) +  math.pow( vertices[0].y - vertices[1].y, 2 ) )
                direction = [ (vertices[0].x - vertices[1].x), (vertices[0].y - vertices[1].y) ]
                if not vertices[0].selected:
                    vertices[0].x = vertices[0].x - direction[0] * distance * attraction
                    vertices[0].y = vertices[0].y - direction[1] * distance * attraction
                if not vertices[1].selected:
                    vertices[1].x = vertices[1].x + direction[0] * distance * attraction
                    vertices[1].y = vertices[1].y + direction[1] * distance * attraction
        elif (self.physics_type==1):
            
            c_1=2#attraction
            c_2=100#max(spacing,.00001)
            c_3=1
            c_4=.5
            pairs=[edge.vs for edge in self.graph.edges] + [(edge.vs[1],edge.vs[0]) for edge in self.graph.edges]
            for i in xrange(len(vertices)):
                vertex=vertices2[random.randrange(0,len(vertices2))]
                vertices2.remove(vertex)
                for vertex2 in vertices2:
                    if not (vertex, vertex2) in pairs:
                        x_distance = vertex.x - vertex2.x
                        y_distance = vertex.y - vertex2.y
                        distance2 = (x_distance * x_distance) +  (y_distance * y_distance)
                        distance = math.sqrt(distance2)
                        if  (vertex.x != vertex2.x or vertex.y != vertex2.y):
                            if x_distance != 0:
                                delta_x = x_distance/distance *c_4 *c_3 / math.sqrt(distance)
                                if not vertex.selected:
                                    vertex.x = vertex.x + delta_x
                                if not vertex2.selected:
                                    vertex2.x = vertex2.x - delta_x
                            if y_distance != 0:
                                delta_y = y_distance/distance *c_4 *c_3 / math.sqrt(distance)
                                if not vertex.selected:
                                    vertex.y = vertex.y + delta_y
                                if not vertex2.selected:
                                    vertex2.y = vertex2.y - delta_y

            for edge in self.graph.edges:
                vertices = edge.vs
                distance = math.sqrt( math.pow( vertices[0].x - vertices[1].x, 2 ) +  math.pow( vertices[0].y - vertices[1].y, 2 ) )
                if (not distance == 0):
                    direction = [ (vertices[0].x - vertices[1].x)/distance, (vertices[0].y - vertices[1].y)/distance ]
                    if not vertices[0].selected:
                        vertices[0].x = vertices[0].x - direction[0] * c_1 *math.log(distance/ c_2)
                        vertices[0].y = vertices[0].y - direction[1] * c_1 *math.log(distance/ c_2)
                    if not vertices[1].selected:
                        vertices[1].x = vertices[1].x + direction[0] * c_1 *math.log(distance/ c_2)
                        vertices[1].y = vertices[1].y + direction[1] * c_1 *math.log(distance/ c_2)
        elif (self.physics_type==2):
            if len(vertices)>1:
                k =.5*math.sqrt(self.area/len(vertices))
                #pairs=[edge.vs for edge in self.graph.edges] + [(edge.vs[1],edge.vs[0]) for edge in self.graph.edges]
                dispx=[0]*len(vertices)
                dispy=[0]*len(vertices)
                for i in xrange(len(vertices)):
                    vertex=vertices2[random.randrange(0,len(vertices2))]
                    vertices2.remove(vertex)
                    for vertex2 in vertices2:
                       # if not (vertex, vertex2) in pairs:
                        x_distance = vertex.x - vertex2.x
                        y_distance = vertex.y - vertex2.y
                        distance2 = (x_distance * x_distance) +  (y_distance * y_distance)
                        distance = math.sqrt(distance2)
                        if  (vertex.x != vertex2.x or vertex.y != vertex2.y):
                            if x_distance != 0:
                                
                                if not vertex.selected:
                                    #disp[i] += x_distance/distance * k*k/distance
                                    dispx[vertices.index(vertex)] += x_distance/distance2 * k*k
                                    #print x_distance/distance2 
                                if not vertex2.selected:
                                    #vertex2.x = vertex2.x - delta_x
                                    dispx[vertices.index(vertex2)] -= x_distance/distance2 * k*k
                            if y_distance != 0:
                                #delta_y = y_distance/distance *c_4 *c_3 / math.sqrt(distance)
                                if not vertex.selected:
                                    #vertex.y = vertex.y + delta_y
                                    dispy[vertices.index(vertex)] += y_distance/distance2 * k*k
                                if not vertex2.selected:
                                    #vertex2.y = vertex2.y - delta_y
                                    dispy[vertices.index(vertex2)] -= y_distance/distance2 * k*k

                for edge in self.graph.edges:
                    evertices = edge.vs
                    distance2 = math.pow( evertices[0].x - evertices[1].x, 2 ) +  math.pow( evertices[0].y - evertices[1].y, 2 )
                    distance = math.sqrt( distance2 )
                    if (not distance == 0):
                        direction = [ (evertices[0].x - evertices[1].x)/distance, (evertices[0].y - evertices[1].y)/distance ]
                        if not evertices[0].selected:
                            dispx[vertices.index(evertices[0])] -= direction[0]*distance2/k
                            dispy[vertices.index(evertices[0])] -= direction[1]*distance2/k
                            
                            #vertices[0].x = vertices[0].x - direction[0] * c_1 *math.log(distance/ c_2)
                            #vertices[0].y = vertices[0].y - direction[1] * c_1 *math.log(distance/ c_2)
                        if not evertices[1].selected:
                            dispx[vertices.index(evertices[1])] += direction[0]*distance2/k
                            dispy[vertices.index(evertices[1])] += direction[1]*distance2/k
                            #vertices[1].x = vertices[1].x + direction[0] * c_1 *math.log(distance/ c_2)
                            #vertices[1].y = vertices[1].y + direction[1] * c_1 *math.log(distance/ c_2)
                #print dispx,dispy,
                for i in xrange(len(vertices)):
                    if not dispx[i]==0 or not dispy[i]==0:
                        vertex= vertices[i]
                        dist= math.sqrt(math.pow( dispx[i] , 2 ) +  math.pow( dispy[i], 2 ))
                        vertex.x += dispx[i]/dist * min(abs(dispx[i]), self.temperature)
                        vertex.y += dispy[i]/dist * min(abs(dispy[i]), self.temperature)
                self.keep_inbounds=True
               # print "temp:", self.temperature
                self.temperature = .99 *self.temperature
        
                
        elif (self.physics_type==3):
            pairs=[edge.vs for edge in self.graph.edges] + [(edge.vs[1],edge.vs[0]) for edge in self.graph.edges]
            if len([1 for vert in vertices if vert.selected])>2:
                for vertex in vertices:
                    if not vertex.selected:
                        sumx=0
                        sumy=0
                        n=0
                        for pair in pairs:
                            if (pair[0] == vertex):
                                sumx+=pair[1].x
                                sumy+=pair[1].y
                                n+=1
                        if n>1:
                            vertex.x=sumx/n
                            vertex.y=sumy/n
                
        if (self.keep_inbounds):
            for v in vertices:
                v.x = min( self.ca_width/2, max( -self.ca_width/2, v.x))
                v.y = min( self.ca_height/2, max( -self.ca_height/2, v.y))
                        
        self.redraw()
        
    def toggle_physics(self, event=None):
        if self.stop_physics:
            self.stop_physics = False
            #print self.regular_buttons[12].image
            #self.regular_buttons[12].image=PhotoImage(file="icons/stopphy.gif")
            self.regular_buttons[12].image.configure(file = "icons/stopphy.gif")
            self.regular_buttons[12].configure(relief = SUNKEN)
            #print self.regular_buttons[12].image
            while(1):
                self.do_physics()
                self.update()
                self.redraw()
                if self.stop_physics == True:
                    return
        else:
            self.stop_physics=True
            self.regular_buttons[12].image.config(file = "icons/startphy.gif")
            self.regular_buttons[12].config(relief = RAISED)
        
    def change_physics(self,event=None):
        if event.keysym == "Up":
            self.spacing+=.5
        elif event.keysym == "Down":
            self.spacing-=.5
        elif event.keysym == "Right":
            self.attraction+=.00001
        elif event.keysym == "Left":
            self.attraction-=.00001
            
    def change_physics_type(self, event=None):
        self.physics_type= (self.physics_type+1)%NUMPHYSICSTYPES
        print "changed physics to type:",self.physics_type

    def drawbox(self):
        center = self.get_center()
        
        if self.box:
            b0 = self.box[0] + center[0]
            b1 = self.box[1] + center[1]
            b2 = self.box[2] + center[0]
            b3 = self.box[3] + center[1]
            self.canvas.create_rectangle(b0, b1, b2, b3, width=2, outline="blue", dash = (2,4), tags="selection box")
            handles = ((b0,b1),
                       (b0,(b1+b3)/2),
                       (b0,b3),
                       (b2,b1),
                       (b2,(b1+b3)/2),
                       (b2,b3),
                       ((b0+b2)/2,b1),
                       ((b0+b2)/2,b3))
            self.handles = {}
            for handle in handles:
                h = self.canvas.create_rectangle(handle[0]-3, handle[1]-3, handle[0]+3, handle[1]+3, fill="blue", outline="blue")
                self.handles[h]=(handle[0],handle[1])

    def drawgrid(self):
        if self.snap_mode.get() == "rect":
            width = float(self.canvas.winfo_width())
            height = float(self.canvas.winfo_height())
            try:
                grid_size = float(self.grid_size.get())
            except:
                print "Error in snap parameters!"
                return
            x = ( (width / 2.0) % grid_size)
            y = ( (height / 2.0) % grid_size)
            while x < width:    #vertical lines
                self.canvas.create_line(x, 0, x, height, width = 1, fill = "grey", tags = "grid")
                x = x + grid_size
            while y < height:    #horizontal lines
                self.canvas.create_line(0, y, width, y, width = 1, fill = "grey", tags = "grid")
                y = y + grid_size
            self.canvas.create_line(0, height/2, width, height/2, width = 2, fill = "grey", tags = "grid")
            self.canvas.create_line(width/2, 0, width/2, height, width = 2, fill = "grey", tags = "grid")
        elif self.snap_mode.get() == "polar":
            width = float(self.canvas.winfo_width())
            height = float(self.canvas.winfo_height())
            center = [width / 2, height / 2]
            #grid_size = float(self.snap_grid_size)
            #number_per_circle = float(self.snap_number_per_circle)
            try:
                grid_size = float(self.grid_size.get())
                number_per_circle = float(self.number_per_circle.get())
            except:
                print "Error in snap parameters!"
                return
            theta = 2 * pi / number_per_circle
            radius = grid_size
            angle = 0
            canvas_radius = sqrt( height * height + width * width ) / 2
            while radius < canvas_radius:
                self.canvas.create_oval(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius, width = 1, outline = "grey", tags = "grid")
                radius = radius + grid_size
            while angle < 2*pi:
                self.canvas.create_line(center[0], center[1], center[0] + canvas_radius * cos(angle), center[1] + canvas_radius * sin(angle), width = 1, fill = "grey", tags = "grid")
                angle = angle + theta

    def snap(self, event, vertex):
        center = self.get_center()
        x = event.x - center[0]
        y = event.y - center[1]
        #grid_size = float(self.snap_grid_size)
        #number_per_circle = float(self.snap_number_per_circle)
        try:
            grid_size = float(self.grid_size.get())
            
        except:
            print "Error in snap parameters!"
            return
                
        if self.snap_mode.get() == "rect":
            low = grid_size * floor( x / grid_size )
            high = grid_size * ceil( x / grid_size )
            if (x - low) < (high - x):
                vertex.x = low
            else:
                vertex.x = high
            low = grid_size * floor( y / grid_size )
            high = grid_size * ceil( y / grid_size )
            if (y - low) < (high - y):
                vertex.y = low
            else:
                vertex.y = high
        elif self.snap_mode.get() == "polar":
        
            try:
                number_per_circle = float(self.number_per_circle.get())
            except:
                print "Error in snap parameters!"
                return
                
            distance = sqrt( x*x + y*y )
            angle = atan2( y, x )

            angle = angle / (2*pi) * number_per_circle

            low = grid_size * floor( distance / grid_size )
            high = grid_size * ceil( distance / grid_size )
            if (distance - low) < (high - distance):
                distance = low
            else:
                distance = high

            low = floor( angle )
            high = ceil( angle )
            if (angle - low) < (high - angle):
                angle = low
            else:
                angle = high

            angle = angle / number_per_circle * 2*pi
            vertex.x = distance * cos( angle )
            vertex.y = distance * sin( angle )

    def select_subgraph(self, type):
        # first, save the old state, and  "pop up" the button
        
        for subgraph in self.subgraph_buttons:
            if subgraph.name == self.selected_subgraph:
                subgraph.config(relief = RAISED)
                for i in range(len(subgraph.options)):
                    subgraph.options[i][1] = self.subgraph_entries[i][1].get()
                    self.subgraph_entries[i][1].delete(0, END)
                    # TODO: should we have done int conversion here?  Make sure we try/except later...(watch out for "file")
                break
        
        # update the selected subgraph
        self.selected_subgraph = type
        
        # update the subgraph entry boxes, and 
        for subgraph in self.subgraph_buttons:
            if subgraph.name == type:
                subgraph.config(relief = SUNKEN)
                self.subgraph_button_frame.pack_forget()
                for i in range(len(subgraph.options)):
                    self.subgraph_entries[i][0].config(text = subgraph.options[i][0])
                    self.subgraph_entries[i][1].config(state = NORMAL)
                    self.subgraph_entries[i][1].insert(END, subgraph.options[i][1])
                    self.subgraph_entries[i][2].pack(side = TOP, anchor = W)
                i = i + 1
                if len(subgraph.options) == 0:
                    i = 0
                while i < len(self.subgraph_entries):
                    self.subgraph_entries[i][0].config(text = "")
                    self.subgraph_entries[i][1].config(state = DISABLED)
                    self.subgraph_entries[i][2].config(height = 0)
                    self.subgraph_entries[i][2].pack_forget()
                    
                    i=i+1
                
                self.subgraph_button_frame.pack(side = TOP)
                break
        
    def insert_subgraph(self):
        for subgraph in self.subgraph_buttons:
            if subgraph.name == self.selected_subgraph:
                options = []
                for i in range(len(subgraph.options)):
                    try:
                        option = int(self.subgraph_entries[i][1].get())
                        if option <= 0:
                            tkMessageBox.showwarning("Invalid Parameters", "All parameters should be positive!")
                            return
                        options.append(option)
                    except:
                        try:
                            option= [int(x) for x in self.subgraph_entries[i][1].get().split(',')]
                            options.append(option)
                        except:                            
                            tkMessageBox.showwarning("Invalid Parameters", "All parameters should be integers!")
                            return
                    
                break
                
        if self.selected_subgraph == "file":
            file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
            if file != None:
                tempgraph = pickle.load(file)
                file.close()
                self.copied_verts = []
                self.copied_edges = []
                for v in tempgraph.vertices:
                    self.copied_verts.append((v.x,v.y,v.label))
                for e in tempgraph.edges:
                    self.copied_edges.append(((e.vs[0].x,e.vs[0].y),(e.vs[1].x,e.vs[1].y),[e.wrap,e.curved,e.height,e.direction]))
                center = self.get_center()
                center = FakeEvent(center[0],center[1])
                self.insert_copied(center)
                self.redraw()
                return
            tkMessageBox.showwarning("Unable to Insert", "No File Chosen")
            return
        
        res = generate.generate(subgraph.name, options)
        if res[0] == "ERROR":
            tkMessageBox.showwarning("Invalid Parameters", res[1])
        self.copied_verts = res[0]
        self.copied_edges = res[1]
        center = self.get_center()
        center = FakeEvent(center[0],center[1])
        self.insert_copied(center)
        self.redraw()
        
    def message(self, title, message, function, type="okcancel"):
        if type=="passgraphokcancel":
            res = tkSimpleDialog.askinteger(title, message)
            if res != None:
                function( self.graph, res )

        if type=="okcancel":
            res = tkSimpleDialog.askinteger(title, message)
            if res != None:
                function( res )

        if type=="Decimal":
            res = tkSimpleDialog.askstring(title, message)
            if res != None:
                function( Decimal(res) )

        elif type=="yesnocancel":
            if tkMessageBox._show(title,message,icon=tkMessageBox.QUESTION,type=tkMessageBox.YESNOCANCEL)=="yes":
                function()

    # def toggle_snap_mode(self, type=None):
        # if type == "none":
            # self.snap_on = False
            # try:
                # self.canvas.delete("grid")
            # except:
                # pass
        # elif type == "rect":
            # self.snap_on = True
            # self.snap_mode = "rect"
        # elif type == "circular":            
            # self.snap_on = True
            # self.snap_mode = "circular"
        
        # self.redraw()
        # return

    def clear(self, reset=True):
        if reset:
            self.registerwithundo()
            self.graph.vertices=[]
            self.graph.edges=[]
            self.graph.tags=[]
        self.canvas.delete("all")

    # event is needed so that it can be called from the "Configure" binding that detects window size changes.
    def redraw(self, event=None):
        self.clear(False)
        self.drawgrid()
        self.graph.draw(self.canvas)
        self.drawbox()

    def get_center(self):
        width = float(self.canvas.winfo_width())
        height = float(self.canvas.winfo_height())
        return [width / 2, height / 2]

def main(update = False):
    warnings.filterwarnings("ignore")
   # import cProfile
    try:
        psyco.full()
    except:
        print "Problem with your psyco. go install it for faster action."
    if update:
        #Update "start.py"
        from shutil import move
        move("start.py.new","start.py")
    world = GraphInterface()
   # cProfile.run('GraphInterface()')
    #world.mainloop()

if __name__ == '__main__':
    main()
