#!/usr/bin/python

import time
import random
from math import *

try:
    import Image, ImageDraw, ImageFont
except:
    pass
import os

def midpoint((x1,y1),(x2,y2)):
    ptx = (x1+x2)/2
    pty = (y1+y2)/2
    return (ptx,pty)

class Component:
    def __init__(self):
        self.selected=False
        self.id=str(time.clock())
        self.color="black"
        self.size=3

    def toggle(self):
        self.selected=not self.selected

class Vertex(Component):
    def __init__(self, (x, y),label="NULL",labelpos=(-12,-12)):
        Component.__init__(self)
        self.x=x
        self.y=y
        self.label=label
        (lx,ly)=labelpos
        self.lx=lx
        self.ly=ly
        self.text=None
        self.color="#ffffff"
        self.lcolor="black"
        self.size=5
        self.lsize=16
        self.shape=0

    def get_center(self, canvas):
        width = float(canvas.winfo_width())
        height = float(canvas.winfo_height())
        return [width / 2, height / 2]

    def draw(self, canvas):
        center = self.get_center(canvas)
        x = center[0] + self.x
        y = center[1] + self.y
        if self.selected:
            self.create_shape(canvas,addsize=3, fill="cyan", tags='select'+str(self.id), width = 0)
        else:
            canvas.delete('select'+str(self.id))
##        try:
        if self.color=="#ffffff" or self.color =="white":
            self.create_shape(canvas,addsize=1, fill="black", activefill="blue", tags=(self.id,"vertex"), width = 0)
        self.circle = self.create_shape(canvas,addsize=0, fill=self.color, activefill="blue", tags=(self.id,"vertex"), width = 0)
##        except:
##            self.color="red"
##            self.size=5
##            self.circle = canvas.create_oval(x-self.size, y-self.size, x+self.size, y+self.size, fill=self.color, activefill="blue", tags=(self.id,"vertex"), width = 0)
        if self.label!="NULL":
            try:
                self.text=canvas.create_text(x+self.lx, y+self.ly, text=str(self.label), tags="label", font="Arial "+str(self.lsize)+" bold", fill=self.lcolor)
            except:
                self.lx=-12
                self.ly=-12
                self.lcolor="magenta"
                self.lsize=16
                self.text=canvas.create_text(x+self.lx, y+self.ly, text=str(self.label), tags="label", font="Arial 16 bold", fill=self.lcolor)
                
    def create_shape(self,canvas,addsize=0, fill="", activefill="",tags="", width = 0):
        center = self.get_center(canvas)
        x = center[0] + self.x
        y = center[1] + self.y
        c=0
        if type(self.shape)==type('A'):
            l=self.size*2+addsize*2
            c=canvas.create_text(x, y,
                               text=str(self.shape), font="Arial "+str(l)+" bold",
                               fill=fill, activefill=activefill,
                               tags=(self.id,"vertex"), width = width)
        elif self.shape==0:
            c=canvas.create_oval(x-self.size-addsize, y-self.size-addsize,
                               x+self.size+addsize, y+self.size+addsize,
                               fill=fill, activefill=activefill,
                               tags=(self.id,"vertex"), width = width)
        elif self.shape==1:
            l=self.size*1.5+addsize*2
            poly=[(x-l*0.866025,y+l/2),(x+l*0.866025,y+l/2),(x,y-l)]
            c=canvas.create_polygon(poly,
                               fill=fill, activefill=activefill,
                               tags=(self.id,"vertex"), width = width)
        elif self.shape==2:
            c=canvas.create_rectangle(x-self.size-addsize, y-self.size-addsize,
                               x+self.size+addsize, y+self.size+addsize,
                               fill=fill, activefill=activefill,
                               tags=(self.id,"vertex"), width = width)
        elif self.shape==3:
            l=(self.size+addsize)*1.41
            poly=[(x-l,y),(x,y+l),(x+l,y),(x,y-l)]
            c=canvas.create_polygon(poly,
                               fill=fill, activefill=activefill,
                               tags=(self.id,"vertex"), width = width)
        else:
            l=self.size+addsize*2;
            poly=[]
            for i in xrange(self.shape):
                poly.append((x+l*1.5*cos(2.*pi*2*i/(self.shape*2)-pi/2),y+l*1.5*sin(2.*pi*2*i/(self.shape*2)-pi/2)))
                poly.append((x+l*.5*cos(2.*pi*(2*i+1)/(self.shape*2)-pi/2),y+l*.5*sin(2.*pi*(2*i+1)/(self.shape*2)-pi/2)))
            c=canvas.create_polygon(poly,
                               fill=fill, activefill=activefill,
                               tags=(self.id,"vertex"), width = width)
        return c
    
    def draw_to_PIL(self, canvas, width, height):
        center = [width/2, height/2]
        x = center[0] + self.x
        y = center[1] + self.y
        if self.selected:
            canvas.ellipse((x-self.size-3, y-self.size-3, x+self.size+3, y+self.size+3), fill="cyan")
        try:
            if self.color=="#ffffff" or self.color=="white":
                canvas.ellipse((x-self.size-1, y-self.size-1, x+self.size+1, y+self.size+1), fill="black")
            canvas.ellipse((x-self.size, y-self.size, x+self.size, y+self.size), fill=self.color)
        except:
            self.color="red"
            self.size=5
            canvas.ellipse((x-self.size, y-self.size, x+self.size, y+self.size), fill=self.color)
        if self.label!="NULL":
            fontdir = os.path.join(os.environ["windir"], "fonts")
            font=ImageFont.truetype(os.path.join(fontdir,u'ARIALBD.TTF'),self.lsize)
            try:
                canvas.text((x+self.lx, y+self.ly-8), text=str(self.label), font=font, fill=self.lcolor)
            except:
                self.lx=-12
                self.ly=-12
                self.lcolor="magenta"
                self.lsize=16
                canvas.text((x+self.lx, y+self.ly-8), text=str(self.label), font=font, fill=self.lcolor)
        return canvas
    
class Edge(Component):
    def __init__(self, v1, v2, selected = False, props = None):
          
        if props: #Allows using "connect" with properties of the edges to be created (wrap, curve, etc.)
            try:
                (wrap, curved, height, direction) = props
            except:
                print "Error with Edge Properties!!!!"
        else:
            curved = False
            wrap = False
            height = 5
            direction = 1
        self.vs=[v1, v2]
        self.selected = selected
        self.curved = curved
        self.wrap = wrap
        self.height = height
        self.direction = direction
        Component.__init__(self)

    def get_center(self, canvas):
        width = float(canvas.winfo_width())
        height = float(canvas.winfo_height())
        return [width / 2, height / 2]

    # Design decision: curve+wrap doesn't exist.
    def draw(self, canvas):
        center = self.get_center(canvas)
        x1 = center[0] + self.vs[0].x
        y1 = center[1] + self.vs[0].y
        x2 = center[0] + self.vs[1].x
        y2 = center[1] + self.vs[1].y

        if self.curved:
            (ptx,pty) = midpoint((self.vs[0].x,self.vs[0].y),(self.vs[1].x,self.vs[1].y))
            angle = atan2(self.vs[0].y-self.vs[1].y,self.vs[1].x-self.vs[0].x)
            
            ptx += self.direction*sin(angle)*self.height
            pty += self.direction*cos(angle)*self.height
            self.curve_through(ptx, pty)

        # This seems redundant, but is in case the curve exits out when curve_through returns False (really a straight line)            
        if self.curved:    
            h = center[0] + self.h
            k = center[1] + self.k
            
            if self.selected:
                canvas.create_arc(h-self.r, k-self.r, h+self.r, k+self.r, style = "arc", width = self.size+4, outline = "red", start = self.start, extent = self.extent, tags = 'select'+str(self.id) )
            else:
                canvas.delete('select'+str(self.id))
            try:
                self.line = canvas.create_arc(h-self.r, k-self.r, h+self.r, k+self.r, style = "arc", width = self.size, outline = self.color, activefill="blue", start = self.start, extent = self.extent, tags = (self.id,"edge") )
            except:
                self.color="black"
                self.size=5
                self.line = canvas.create_arc(h-self.r, k-self.r, h+self.r, k+self.r, style = "arc", width = self.size, outline = self.color, activefill="blue", start = self.start, extent = self.extent, tags = (self.id,"edge") )
        else:
            if self.wrap:
                width = float(canvas.winfo_width())
                height = float(canvas.winfo_height())
                smallest = -1
                coords2 = [0,0]
                for (i,j) in [[-1,0],[1,0],[0,-1],[0,1]]:  # We don't want to wrap to diagonal "imaginary boxes", because then part of the line is not visible.
                    x2temp = width*i + x2
                    y2temp = height*j + y2
                    dist = pow(pow(x1 - x2temp,2)+pow(y1 - y2temp,2),.5)
                    if smallest == -1 or dist < smallest:
                        smallest = dist
                        coords = [i, j]
                x1new = x1-width*coords[0]
                y1new = y1-height*coords[1]
                x2new = x2+width*coords[0]
                y2new = y2+height*coords[1]
            if self.selected:
                if self.wrap:
                    canvas.create_line(x1, y1, x2new, y2new, width=self.size+4, fill="red", tags='select'+str(self.id))
                    canvas.create_line(x1new, y1new, x2, y2, width=self.size+4, fill="red", tags='select'+str(self.id))
                else:
                    canvas.create_line(x1, y1, x2, y2, width=self.size+4, fill="red", tags='select'+str(self.id))
            else:
                canvas.delete('select'+str(self.id))
            if self.wrap:
                try:
                    self.line = canvas.create_line(x1, y1, x2new, y2new, tags=(self.id,"edge"), width=self.size, activefill="blue",fill=self.color)
                    self.altline = canvas.create_line(x1new, y1new, x2, y2, tags=(self.id,"edge"), width=self.size, activefill="blue",fill=self.color)
                except:
                    self.color="black"
                    self.size=5;
                    self.line = canvas.create_line(x1, y1, x2new, y2new, tags=(self.id,"edge"), width=self.size, activefill="blue",fill=self.color)
                    self.altline = canvas.create_line(x1new, y1new, x2, y2, tags=(self.id,"edge"), width=self.size, activefill="blue",fill=self.color)
            else:
                try:
                    self.line = canvas.create_line(x1, y1, x2, y2, tags=(self.id,"edge"), width=self.size, activefill="blue",fill=self.color)
                except:
                    self.color="black"
                    self.size=5
                    self.line = canvas.create_line(x1, y1, x2, y2, tags=(self.id,"edge"), width=self.size, activefill="blue",fill=self.color)
                    
    def draw_to_PIL(self, canvas, width, height):
        center = [width/2, height/2]
        x1 = center[0] + self.vs[0].x
        y1 = center[1] + self.vs[0].y
        x2 = center[0] + self.vs[1].x
        y2 = center[1] + self.vs[1].y
        
        if self.curved:
            (ptx,pty) = midpoint((self.vs[0].x,self.vs[0].y),(self.vs[1].x,self.vs[1].y))
            angle = atan2(self.vs[0].y-self.vs[1].y,self.vs[1].x-self.vs[0].x)
            
            ptx += self.direction*sin(angle)*self.height
            pty += self.direction*cos(angle)*self.height
            self.curve_through(ptx, pty)

        # This seems redundant, but is in case the curve exits out when curve_through returns False (really a straight line)            
        if self.curved:    
            h = center[0] + self.h
            k = center[1] + self.k
            end=(360-self.extent-self.start)%360
            start=(360-self.start)%360
            if (self.direction>0):
                temp=start
                start=end
                end=temp
            if self.selected:
                self.draw_thick_arc(canvas,(h-self.r, k-self.r, h+self.r, k+self.r),  start = start,end = end, fill = "red", width=self.size+4 )
            try:
                self.draw_thick_arc(canvas,(h-self.r, k-self.r, h+self.r, k+self.r),  start = start,end = end, fill = self.color, width=self.size )
            except:
                self.color="red"
                self.draw_thick_arc(canvas,(h-self.r, k-self.r, h+self.r, k+self.r),  start = start,end = end, fill = self.color, width=self.size )
        else:  
            if self.wrap:
                smallest = -1
                coords2 = [0,0]
                for (i,j) in [[-1,0],[1,0],[0,-1],[0,1]]:  # We don't want to wrap to diagonal "imaginary boxes", because then part of the line is not visible.
                    x2temp = width*i + x2
                    y2temp = height*j + y2
                    dist = pow(pow(x1 - x2temp,2)+pow(y1 - y2temp,2),.5)
                    if smallest == -1 or dist < smallest:
                        smallest = dist
                        coords = [i, j]
                x1new = x1-width*coords[0]
                y1new = y1-height*coords[1]
                x2new = x2+width*coords[0]
                y2new = y2+height*coords[1]
            if self.selected:
                if self.wrap:
                    self.draw_thick_line(canvas,(x1, y1, x2new, y2new), width=self.size+4, fill="red")
                    self.draw_thick_line(canvas,(x2new, y2new,x1, y1), width=self.size+4, fill="red")

                    self.draw_thick_line(canvas,(x1new, y1new, x2, y2), width=self.size+4, fill="red")
                    self.draw_thick_line(canvas,(x2, y2,x1new, y1new), width=self.size+4, fill="red")
                else:
                    self.draw_thick_line(canvas,(x1, y1, x2, y2), width=self.size+4, fill="red")
                    self.draw_thick_line(canvas,(x2, y2,x1, y1), width=self.size+4, fill="red")
            if self.wrap:
                self.draw_thick_line(canvas,(x1, y1, x2new, y2new), width=self.size, fill="black")
                self.draw_thick_line(canvas,( x2new, y2new,x1, y1), width=self.size, fill="black")
                self.draw_thick_line(canvas,(x1new, y1new, x2, y2), width=self.size, fill="black")
                self.draw_thick_line(canvas,( x2, y2, x1new, y1new), width=self.size, fill="black")
            else:
                self.draw_thick_line(canvas,(x1, y1, x2, y2),width=self.size, fill="black")
                self.draw_thick_line(canvas,(x2, y2, x1, y1),width=self.size, fill="black")
        return canvas

    #draw thick line on PIL draw object canvas
    #box=4-tuple with x1,y1,x2,y2
    #width=width of line,
    #fill=color
    def draw_thick_line(self,canvas,box,width,fill,res=1.):
##        
##        for i in xrange(width*res+1):
####            print (i/res-width/2.)/sqrt(2)
##            canvas.line((box[0]+i/res-width/2., box[1], box[2]+i/res-width/2., box[3]), width=1,fill = fill )
##            canvas.line((box[0], box[1]+i/res-width/2., box[2], box[3]+i/res-width/2.), width=1,fill = fill )
##            canvas.line((box[0]+(i/res-width/2.)/sqrt(2), box[1]+(i/res-width/2.)/sqrt(2), box[2]+(i/res-width/2.)/sqrt(2), box[3]+(i/res-width/2.)/sqrt(2)), fill = fill )
##            canvas.line((box[0]+(i/res-width/2.)/sqrt(2), box[1]-(i/res-width/2.)/sqrt(2), box[2]+(i/res-width/2.)/sqrt(2), box[3]-(i/res-width/2.)/sqrt(2)), fill = fill )
##            canvas.line((box[0]+(i/res-width/2.)/sqrt(2), box[1]-(i/res-width/2.)/sqrt(2), box[2]-(i/res-width/2.)/sqrt(2), box[3]+(i/res-width/2.)/sqrt(2)), fill = fill )
##            canvas.line((box[0]+(i/res-width/2.)/sqrt(2), box[1]+(i/res-width/2.)/sqrt(2), box[2]-(i/res-width/2.)/sqrt(2), box[3]-(i/res-width/2.)/sqrt(2)), fill = fill )
        if box[2]!=box[0]:
            slope=(float(box[3]-box[1]))/float(box[2]-box[0])
            y=width/2./sqrt(slope**2+1)
            x=-y*slope
        else:
            y=0
            x=width/2.
        
        canvas.polygon([(box[0]+x,box[1]+y),(box[0]-x,box[1]-y),
                        (box[2]-x,box[3]-y),(box[2]+x,box[3]+y)],fill=fill)
    
    def draw_thick_arc(self, canvas, box, start, end, fill="black", width=5,res=5.):
            for i in xrange(width*res):
                canvas.arc((box[0]+i/res-width/2., box[1], box[2]+i/res-width/2., box[3]),  start = start,end = end, fill = fill )
                canvas.arc((box[0], box[1]+i/res-width/2., box[2], box[3]+i/res-width/2.),  start = start,end = end, fill = fill )
                canvas.arc((box[0]+(i/res-width/2.)/sqrt(2), box[1]+(i/res-width/2.)/sqrt(2), box[2]+(i/res-width/2.)/sqrt(2), box[3]+(i/res-width/2.)/sqrt(2)),  start = start,end = end, fill = fill )
                canvas.arc((box[0]+(i/res-width/2.)/sqrt(2), box[1]-(i/res-width/2.)/sqrt(2), box[2]+(i/res-width/2.)/sqrt(2), box[3]-(i/res-width/2.)/sqrt(2)),  start = start,end = end, fill = fill )
                       
    def curve_through(self, x, y):
        self.curved = 1
        x1 = self.vs[0].x
        x2 = self.vs[1].x
        x3 = x
        y1 = self.vs[0].y
        y2 = self.vs[1].y
        y3 = y
        
        # From mathworld.wolfram.  Distance from point to line.
        d = abs((x2-x1)*(y1-y3)-(x1-x3)*(y2-y1))/sqrt(pow(x2-x1,2)+pow(y2-y1,2))
        #TODO: consider 2 to be a better limit? especially on curves large enough to "wrap"
        if -1 < d < 1:
            self.curved = 0
            #TODO: add "wrap detection" to this cool logic...set self.wrapped if it's outside.
            return False
        
        # Note:  The following constants and equations were derived from solving the system of equations for a circle 
        # generated from each (xi,yi) pair above to find the center (h, k) and radius r.
        
        #try:
        C = (-y2+y3)/(x2-x3)
        D = .5*(-pow(x3,2)-pow(y3,2)+pow(x2,2)+pow(y2,2))/(x2-x3)
        #escept:
            #TODO: switch these, and make sure this is valid...
        #    zeroed = 
        #    C1 = (-y1+y3)/(x1-x3)
        self.k = .5*(pow(x1,2)+pow(y1,2)-pow(x2,2)-pow(y2,2)-2*x1*D+2*x2*D)/(C*x1+y1-C*x2-y2)
        self.h = C*self.k + D
        self.r = sqrt(pow(x1-self.h,2)+pow(y1-self.k,2))
        th1 = atan2(self.k-y1,x1-self.h) / pi * 180
        th2 = atan2(self.k-y2,x2-self.h) / pi * 180
        th3 = atan2(self.k-y3,x3-self.h) / pi * 180
        self.start = th1
        if th1 > th3 > th2 or th1 < th3 < th2:
            self.extent = th2-th1
        elif th1 > th2:
            self.extent = 360-(th1-th2)
        else:
            self.extent = -360+(th2-th1)
            
        sep = sqrt(pow(x1-x2,2)+pow(y1-y2,2)) #separation between the endpoints
        
        #These debugging messages are present because of some weird errors of height turning into -1.#IND
        # Didn't fix yet; happened when pressed "up arrow" for a while after inserting hexagon (6 cycle)
        # Perhaps we could deal by implementing a different function for "change height"
        # It appears to just be the three height lines below; try removing them and trying just with the arrows....
        # This works; but then dragging to curve doesn't work.  Fix this sometime.
        
        # print "-----"
        # print "height", self.height
        # print "self.r", self.r
        # print "sep", sep
        
        self.height = self.r - sqrt(pow(self.r,2)-pow(sep/2,2))
        if abs(self.extent) >= 180:
            self.height = self.r*2-self.height
        
        self.direction = abs(self.extent)/self.extent
        # print "-----"
        # print "height", self.height
        # print "dir", self.direction
        # print "k", self.k
        # print "h", self.h
        # print "ext", self.extent
        # print "str", self.start
        
        return True
                
    def create_arc(self, canvas, x1, y1, x2, y2, height, width, color, tags):
        chord = sqrt( (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2) )
        AX = float(x1)
        AY = float(y1)
        BX = float(x2)
        BY = float(y2)
        if height < 0:
            (AX, BX) = (BX, AX)
            (AY, BY) = (BY, AY)
            height = -height
        if 2 * height > chord:
            height = chord / 2
        delta_X = AX - BX
        delta_Y = AY - BY
        delta_Total = delta_X + delta_Y
        midline_angle = atan2( delta_X, delta_Y ) + pi / 2
        chord_midpoint_X = (AX + BX) / 2
        chord_midpoint_Y = (AY + BY) / 2
        radius = (height + chord*chord / (4*height)) / 2
        triangle_height = radius - height
        origin_X = chord_midpoint_X - triangle_height * sin( midline_angle )
        origin_Y = chord_midpoint_Y - triangle_height * cos( midline_angle )
        SX = origin_X - radius
        SY = origin_Y - radius
        TX = origin_X + radius
        TY = origin_Y + radius
        A_delta_X = AX - origin_X
        A_delta_Y = origin_Y - AY
        B_delta_X = BX - origin_X
        B_delta_Y = origin_Y - BY
        A_angle = atan2( A_delta_Y, A_delta_X ) / pi * 180
        B_angle = atan2( B_delta_Y, B_delta_X ) / pi * 180
        if B_angle < 0 and A_angle > 0:
            start = B_angle
            extent = (A_angle - B_angle) - 360
        else:
            start = A_angle
            extent = B_angle - A_angle
        return canvas.create_arc( SX, SY, TX, TY, style = "arc", width = width, outline = color, start = start, extent = extent, tags = tags )

class Graph:
    def __init__(self, vertices = [], edges = [], labelingConstraints = [2,1], tags = []):
        self.vertices = vertices
        self.edges = edges
        self.tags = tags
        self.labelingConstraints = labelingConstraints
        #self.randomGraph();

    def randomGraph(self):
        numverts=random.randint(4,30);
        for i in xrange(numverts):
            self.vertices.append(Vertex((random.randint(-300,300), random.randint(-300,300))))
        numedges = random.randint(numverts/2, numverts*3)
        for i in xrange(numedges):
            self.connect([self.vertices[random.randint(0,numverts-1)], self.vertices[random.randint(0,numverts-1)]])
           
    
    def loadadjlist(self, adjlist):
        numverts = len(adjlist)
        self.vertices = []
        self.edges = []
        for i in range(numverts):
            self.vertices.append(Vertex((100*cos(2.*pi*i/(numverts)),100*sin(2.*pi*i/(numverts)))))
        for i in range(numverts):
            for connectvert in adjlist[i][1:]:
                adjlist[int(connectvert)-1].remove(i+1)
                self.edges.append(Edge(self.vertices[int(connectvert)-1],self.vertices[i]))

    #load a graph based on short code (genreg program output)
    def loadshortcode(self, shortcode, all=True):
        n=shortcode[0]#numverts
        k=shortcode[1]#degree of grap4eh
        i=2;
        previouscode=[]       
        while i<len(shortcode):
            self.vertices = []
            self.edges = []
            for counter in xrange(n):
                self.vertices.append(Vertex((100*cos(2.*pi*counter/(n)),100*sin(2.*pi*counter/(n))))) 
            numsame=shortcode[i]
            i+=1
            currentcode=[]
            if numsame>0:
                currentcode=previouscode[:numsame]
            for j in xrange(k*n/2-numsame):
                currentcode.append(shortcode[i])
                i+=1
            degrees=[0]*n
            j=0
            for currentvertnum in xrange(n):#go through every vertex number from 0 to n-1
                for l in xrange(k-degrees[currentvertnum]):
                    self.edges.append(Edge(self.vertices[currentvertnum],self.vertices[currentcode[j]-1]))
                    degrees[currentcode[j]-1]+=1
                    j+=1
            previouscode=currentcode[:]
            if all==False:
                i=len(shortcode)
            yield self
    #loads a graph based on an adjacency matrix, putting vertices on a m by n grid
    #only works for undirected graph ( for loops don't check other side of symmetric adjacency matrix)
    def loadadjmatrix(self, adj,m=0,n=0,verts1=[], verts2=[]):
        self.vertices=[]
        self.edges= []
        numverts=len(adj)

        if (m!=0 and n!=0 and m*n==numverts):
##            print "m*n="+str(m)+"*"+str(n)+"="+str(m*n)+"=="+str(numverts)
            if len(verts1)!=m or len(verts2)!=n:
                for i in xrange(m):
                    for j in xrange(n):
                        self.vertices.append(Vertex((200.0*i/m-100,200.*j/n-100)))
            else:
                center1=(sum([vert.x for vert in verts1])/m,sum([vert.y for vert in verts1])/m )
                center2=(sum([vert.x for vert in verts2])/n,sum([vert.y for vert in verts2])/n )
                for i in xrange(m):
                    for j in xrange(n):
                        self.vertices.append(Vertex(((verts1[i].x-center1[0])*2+(verts2[j].x-center2[0])*.5,(verts1[i].y-center1[1])*2+(verts2[j].y-center2[1])*.5)))
        else:
##            print "m*n="+str(m)+"*"+str(n)+"="+str(m*n)+"!="+str(numverts)
            for i in xrange(numverts):
                self.vertices.append(Vertex((100*cos(2.*pi*i/(numverts)),100*sin(2.*pi*i/(numverts)))))
        for i in xrange(numverts-1):
            for j in xrange(i+1, len(self.vertices)):
                if adj[i][j]!=0:
                    self.edges.append(Edge(self.vertices[i],self.vertices[j]))
                    
    #loads a GPG from the order as list of ints corresponding to vertex ordering for inner cycle
    def loadGPG(self,order):
        self.vertices=[]
        self.edges=[]
        num=len(order)
        for i in xrange(num):
            self.vertices.append(Vertex((100*cos(2.*pi*i/(num)-pi/2),100*sin(2.*pi*i/(num)-pi/2))))
        for i in xrange(num):   
            self.vertices.append(Vertex((200*cos(2.*pi*i/(num)-pi/2),200*sin(2.*pi*i/(num)-pi/2))))
        for i in xrange(num-1):
            self.edges.append(Edge(self.vertices[i+num],self.vertices[i+1+num]))#outside ring
            self.edges.append(Edge(self.vertices[i],self.vertices[i+num]))#inside to outside
        self.edges.append(Edge(self.vertices[num],self.vertices[-1]))#complete outside ring
        self.edges.append(Edge(self.vertices[num-1],self.vertices[num*2-1]))#complete inside to outside
        for i in xrange(num-1):
            self.edges.append(Edge(self.vertices[order[i]],self.vertices[order[i+1]]))
        self.edges.append(Edge(self.vertices[order[num-1]],self.vertices[order[0]]))
    
    def draw(self, canvas):
        # Draws edges and vertices on graph
        for e in self.edges:
            e.draw(canvas)
        for v in self.get_vertices():
            v.draw(canvas)
    def draw_to_file(self, draw,width,height):
        for e in self.edges:
            draw=e.draw_to_PIL(draw, width, height)
        for v in self.get_vertices():
            draw=v.draw_to_PIL(draw,width,height)
        return draw
    
    def quickdraw_to_file(self,width=400,height=400):
        image1 = Image.new("RGB", (width, height), (255,255,255))
        draw = ImageDraw.Draw(image1)
        draw=self.draw_to_file(draw,width,height)
        image1.save('boo.png')
        
    def connect(self, vs=None, props=None):
        # Connects vertices in list 'vs'; if none given, connects all selected vertices.
        if not vs:
            vs = [v for v in self.get_vertices() if v.selected]

        for v1 in vs:
            for v2 in vs:
                if v1!=v2:
                    pairs=[edge.vs for edge in self.edges]
                    if [v1,v2] not in pairs and [v2,v1] not in pairs:
                        self.edges.append(Edge(v1, v2, props = props))

#        self.toggle_all()

    def get_vertices( self, vertices = None ):
        just_vertices = []
        active_vertices = vertices or self.vertices
        for element in active_vertices:
            if type(element) == type([]):
                if element != []:                  # TODO: shouldn't need this unless generate creates empty set
                    just_vertices = just_vertices + self.get_vertices(element)
            elif type(element) == type( Vertex( (0,0) ) ):
                just_vertices = just_vertices + [element]
            else:
                print "who put the cookie in the vertex jar?"
        return just_vertices

    def remove_vertex( self, vertex ):
        self.tags = []
        self.vertices = self.get_vertices()
        self.vertices.remove(vertex)

    def add_vertex( self, vertex, vertices = None, level = 0 ):
        self.tags = []
        self.vertices = self.get_vertices()
        self.vertices.append(vertex)
