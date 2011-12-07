from math import ceil
from copy import deepcopy
from decimal import Decimal # Only for comparison in auto_label function!
import random
try:
    from numpy.linalg import eig
except:
    print("You don't have numpy! No eigenvalues for you!")
#import psyco
#psyco.full()

# Works with reals
# Creates an adjacency matrix for the vertex and egde list passed.  Relies on the format of vertices and edges.
def adjacencymatrix(verts,edges):
#    verts = self.graph.get_vertices()
#    edges = self.graph.edges
    size = len(verts)
    row = [0]*size
    adj = []
    for i in range(size):
        adj.append(list(row))
    for edge in edges:
        v1 = verts.index(edge.vs[0])
        v2 = verts.index(edge.vs[1])
        adj[v1][v2] = 1
        adj[v2][v1] = 1
    return adj

#creates the shortcode representation of a regular graph
#no leading 0 for the number of repeated elements from previous code
#no n,k beginning encryption
def generate_shortcode(verts,edges):
    n=len(verts)
    code=[]
    for vert in verts:
        connected=[]
        for edge in edges:
            if vert in edge.vs:
                biggest=max([verts.index(edge.vs[0]),verts.index(edge.vs[1])])
                if biggest!=verts.index(vert):
                    connected.append(biggest+1)
        connected.sort()
        for c in connected:
            code.append(c)
    return code

#determines if a graph G(verts, edges) is regular (same degree for each vertex)
def is_regular(verts,edges):
    degrees=[0]*len(verts)
    for edge in edges:
        degrees[verts.index(edge.vs[0])]+=1
        degrees[verts.index(edge.vs[1])]+=1
    return len(set(degrees))==1
    
#PRODUCTS
#create identity matrix of size m
def identity(m=1):
    return [[int(i==j) for i in range(m)] for j in range(m)]
#Computes the tensor (cross) product adjacency matrix from two adjacency matrices
def tensor_product(adj1, adj2):
    m=len(adj1)
    n=len(adj1[0])
    p=len(adj2)
    q=len(adj2[0])
    resadj=[]
    for i in xrange(m*p):
        resadj.append([None]*(n*q))
    for i in xrange(m):
        for j in xrange(n):
            for k in xrange(p):
                for l in xrange(q):
                    resadj[i*p+k][j*q+l]=adj1[i][j]*adj2[k][l]
    return resadj
def cartesian_product(adj1, adj2):
    return matrix_addition(tensor_product(adj1,identity(len(adj2))),tensor_product(identity(len(adj1)),adj2))
def strong_product(adj1,adj2):
    return matrix_addition(cartesian_product(adj1,adj2),tensor_product(adj1,adj2))

# Works with reals
# Creates a list with the labels of all vertices
def labels(verts):
    return [vert.label for vert in verts]

# Works with reals
# Creates a matrix with vertices vs. vertices where the intersection an vertex x and vertex y is the shortest path from x to y.
# Completes this via a Breadth First Search to find paths for each vertex
def shortestpathmatrix(verts,edges):
    adj = adjacencymatrix(verts,edges)
#    verts = self.graph.get_vertices()
    size = len(verts)
    for vert in range(size):
        i = 2
        A = [vert]
        B = range(size)
        B.remove(vert)
        A = neighbors(adj,A,B)
        for a in A:
            B.remove(a)
        while B != [] and A != []:
            A = neighbors(adj,A,B)
            for a in A:
                adj[vert][a] = i
                adj[a][vert] = i
                B.remove(a)
            if A == []:
                for b in B:
                    adj[vert][b] = -1
                    adj[b][vert] = -1
            i=i+1
    return adj

def adjacencyToDist2Matrix(adj):
    if (len(adj) == 0):
        return list(adj)
    l2m = [ list(r) for r in adj]
    adj2 = matrixmult(adj, adj)
    for i in range(len(adj2[0])):
        for j in range(len(adj2)):
            adj2[i][j] = 2*int(adj2[i][j]>0)
            if adj[i][j]:
                adj2[i][j] = 1
            if (i == j):
                adj2[i][j] = 0
    return adj2

# multiplies matrices
def matrixmult(matrix1,matrix2):
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
    else:
        # Multiply if correct dimensionsa
        new_matrix = [[0 for row in range(len(matrix1))] for col in range(len(matrix2[0]))]
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
        return new_matrix
# Works with reals
# Takes in an adjacency matrix and a list "A" and "B" of vertices; returns a list of vertices in B that are adjacent to some vertex in A.
def neighbors(adj,A,B):
    retlist = []
    for b in B:
        nlist = adj[b]
        size = len(nlist)
        for i in range(size):
            if nlist[i] == 1 and i in A:
                retlist.append(b)
                break
    return retlist

# Works with reals
# Checks the current labeling according to the labeling constraints
def check_labeling(verts,edges,constraints):
    size = len(verts)
    spm = shortestpathmatrix(verts,edges)
    cols = labels(verts)
    maxdist = len(constraints)

    #checks vertices using the shortest path matrix
    for i in range(size-1):  # no need to check last vertex, because have checked all other against it.
        for j in range(i+1,size):  # will have covered interaction of all vertices before this one with itself already
            dist = spm[i][j]
            if 0 < dist <= maxdist and cols[i] != 'NULL' and cols[j] != 'NULL':
                # only runs if labeling constraints are concerned with this short of path
                # and if both vertices are labelled.
                # finally, if dist < 0, then vertices are disconnected
                coldist = abs(cols[i]-cols[j])
                if coldist < constraints[dist-1]: #checks the coloring constraints to make sure it works
                    return [False,(i,j)]
                    #TODO: change this to throwing error and catching?

    return True

# Works with reals.
# a simple, no frills algorithm for automatically generating a smallest span labelling
def auto_label(verts, edges, constraints, minmaxlabel, holes_mode = "none"):
    
    if check_labeling(verts,edges,constraints) != True:
        return False
        
    reals = 0
    for constraint in constraints:
        if type(constraint) == type(Decimal(0)):
            reals = 1
            break
    for v in verts:
        if type(v.label) == type(Decimal(0)):
            reals = 1
            break

    if holes_mode == "allow":
#        print "holes allowed"
        final_check = holes_allowed
    elif holes_mode == "none":
#        print "no holes allowed"
        if reals == 1:
            return "RealError"
        final_check = no_holes_allowed
    elif holes_mode == "minimize":
        if reals == 1:
            return "RealError"
#        print "minimize holes"
        final_check = minimize_holes
    else: # # default to holes allowed # # TODO: There is an error if you get this far!!!!
        final_check = holes_allowed

    size = len(verts)
    spm = shortestpathmatrix(verts,edges)
    labs = labels(verts)
#    maxdist = len(constraints)
    maxlabel = minmaxlabel
    # TODO: calculate lower bound of labeling, and test to see if it is better than this person's guess--this may eliminate really long wait
    # TODO: for reals, change from index to actual number
    
    initvertex = 0
    # TODO: is there an optimum place to start?
    

    memory = [None] # memory is a list so that changes made to it's contents will carry out of the methods

    # There was a sketchy error happening if you don't explicitly pass "set=[]".  It just builds the dsets together from each auto-labeling...
    
    d_set = build_d_set(constraints, len(verts), setlist = [])
    d_set=list(d_set)
    d_set.sort()
    # TODO: there's probably a simple way to combine the next two blocks of code.	
    # If the initial vertex is precolored, this doesn't overwrite it
    if labs[initvertex] != 'NULL':
        while 1:
            res = try_label(spm, initvertex, labs[initvertex], maxlabel, labs, constraints, final_check, d_set, memory)
            if res != False:
                return res
            if holes_mode == "minimize" and memory[0] != None:
    #            print memory[0][1]
                return memory[0][1]  # when minimizing
            
            if maxlabel > len(d_set): 
                print "no labeling of the given type can be found."
                raise("hell") # this means no labeling of the given type can be found.
            maxlabel += 1
    # Only executes if the first label is not pre-colored.
    while 1:
#        for label in range(int(ceil(maxlabel/2.))): # only need to try first half of the colors; second half is equivilent. if not prelabeled
        for label in d_set[0:maxlabel+1]:
           # what if initlabel was already labelled??  I think this breaks...
           res = try_label(spm, initvertex, label, maxlabel, labs, constraints, final_check, d_set, memory)
           print res
           if res != False:
               return res
        if holes_mode == "minimize" and memory[0] != None:
#            print memory[0][1]
            return memory[0][1]  # when minimizing
        maxlabel += 1
        if maxlabel > len(d_set):
            print "no labeling of the given type can be found."
            raise("hell")
            raise("hell")
            raise("hell")
    
# completely plays out a k conversion process on a graph until nothing changes
def finishklabeling(verts, edges, k):
    (lmin, lmax,complete)=labeling_difference(verts)
    still_going= not complete
    adj=adjacencymatrix(verts,edges)
    conversiontime=lmax
    while still_going:
        conversiontime+=1
        changelist=stepthrough(verts,adj,k)
        for vertnum in changelist:
            verts[vertnum].label=conversiontime
        still_going=(len(changelist)!=0)
    return [vert.label for vert in verts]

#steps through one step of the k conversion process (k==-1 for majority)
def stepthrough(verts, adj,k):
    changelist=[]
    for i in xrange(len(verts)):
        sum=0
        neighbors=0
        if verts[i].label=="NULL":
            for j in xrange(len(verts)):
                #print "sum+="+str(adj[i][j])+"*"+str(verts[j].label!='0')+" and "+str(verts[j].label!="NULL")+" for "+ str(i)+","+str(j)+" verts[j]:"+str(verts[j].label)
                if (i!=j):
                    sum+=adj[i][j]*(verts[j].label!="NULL")
                neighbors+=adj[i][j]
            if((sum>=k and k>0) or (k==-1 and sum>=neighbors/2.)or (k==-2 and sum>neighbors/2.)):
                changelist.append(i)
    return changelist

#steps through one step of the kpath process (k == -1 for majority not implemented yet)
#
def stepthroughkpath(verts, adj, k):
    changelist=[]
    adj2 = matrixmult(adj, adj)
    for i in xrange(len(verts)):
        for j in xrange(i):
            if ( (adj[i][j] == 0) and (adj2[i][j] >= k)):
                changelist.append([i,j]);
    return changelist

#finds the lowest and highest label in graph, and if the graph is completely covered
def labeling_difference(verts):
    lmax = 0
    lmin = -1
    complete=True
    for vert in verts:
        if type(vert.label)==type('NULL'):
            complete=False
        else:
            if vert.label > lmax:
                lmax = vert.label
            if vert.label < lmin or lmin == -1:
                lmin = vert.label
        
    return (lmin,lmax,complete)

#determines if everything is labeled
def completely_converted(vertlabels):
    for vertlabel in vertlabels:
        if vertlabel=='NULL':
            return False
    return True

def find_conversion_set(verts, edges, k, minsize):
    size=0
    final_set_nums=[]
    for v in verts:
        v.label='NULL'
    degrees=vertexdegrees(verts,edges)
    for i in xrange(len(degrees)):
        if degrees[i]<min(k,1):
            verts[i].selected=True
            verts[i].label=0
            final_set_nums.append(i)
            size+=1
    if k>=0:
        triviallabels=finishklabeling(verts,edges,k)
    else:
        triviallabels = ['NULL' for i in xrange(len(verts))]
    ntvertnums=[]
    for i  in xrange(len(verts)):
        verts[i].label=triviallabels[i]
        if verts[i].label=='NULL':
            ntvertnums.append(i)
            
    for size in xrange(minsize, len(ntvertnums)):
        for sub in k_subsets_i(len(ntvertnums),size):
            unlabeled=ntvertnums[:] 
            for i in xrange(len(verts)):
                verts[i].label=triviallabels[i]
            sub=list(sub)
            print sub
            validset=True;
            for i in xrange(size):
                nv=sub[i]
                verts[unlabeled[nv]].label=0
                trylabels=finishklabeling(verts,edges,k)
                validset=True;
                for j in xrange(i+1,size):
                    # we don't have a min set if one that would be colored is 
                    # initially colored - it doesn't need to be initially
                    # colored
                    if trylabels[sub[j]]!='NULL':
                        validset=False
                        break
                # not sure why this is here.. I think it breaks above
                if not validset:
                    break
            
            if 'NULL' not in trylabels:
                # clear all labels, then set labels to 0 for the ones that work
                labels=['NULL']*len(verts)
                for num in final_set_nums+sub:
                    labels[num]=0
                return labels
    print "couldn't find a conversion set"
    return False
#copmutes n choose k    
def k_subsets_i(n, k):
    '''
    Yield each subset of size k from the set of intergers 0 .. n - 1
    n -- an integer > 0
    k -- an integer > 0
    '''
    # Validate args
    if n < 0:
        raise ValueError('n must be > 0, got n=%d' % n)
    if k < 0:
        raise ValueError('k must be > 0, got k=%d' % k)
    # check base cases
    if k == 0 or n < k:
        yield set()
    elif n == k:
        yield set(range(n))

    else:
        # Use recursive formula based on binomial coeffecients:
        # choose(n, k) = choose(n - 1, k - 1) + choose(n - 1, k)
        for s in k_subsets_i(n - 1, k - 1):
            s.add(n - 1)
            yield s
        for s in k_subsets_i(n - 1, k):
            yield s
#returns list with elements matching verts with number of edges going out from vertex
#vertexdegrees(verts,edges)[0]== degree of verts[0]
def vertexdegrees(verts,edges):
    degrees=[0]*len(verts)
    for edge in edges:
        v1 = verts.index(edge.vs[0])
        v2 = verts.index(edge.vs[1])
        degrees[v1]+=1
        degrees[v2]+=1
    return degrees
#TODO: add subgraph minimums; subgraph colorings, etc.  Don't try same over and over again!
#TODO: order of coloring attempts (vertex order): in order of highest to lowest connections?
#TODO: find faster method for lambda number than actually labeling

# Works with reals
# doesn't check for holes
def holes_allowed(labels, maxlabel, memory):
#    print "holes"
    return labels

# Fundamentally flawed for reals; can't have holes/nonholes with reals.
# checks for holes, continues if holes are present
def no_holes_allowed(labels, maxlabel, memory):
#    print "noholes"
    labels_used = [False] * (maxlabel + 1)
    for entry in labels:
        labels_used[entry] = True
    full = True
    index = 0
    while full and index < maxlabel + 1:
        full = full and labels_used[index]
        index += 1
    # TODO: simplify calculation of 'full' by just multiplying all indices, or checking if there is a zero, perhaps through a min(list) function?
    if full:
        return labels
    else:
        return False

# Fundamentally flawed for reals; can't have holes/nonholes with reals.
# looks for minimal holes
def minimize_holes(labels, maxlabel, memory):
#    print "minholes"
    labels_used = [0] * (maxlabel + 1)
    for entry in labels:
        labels_used[entry] = 1
    number_of_labels = sum(labels_used)
#    print number_of_labels
    if number_of_labels == maxlabel + 1:
        return labels
    else:
        if memory[0] == None or number_of_labels > memory[0][0]: # Shouldn't we be checking number of holes? (actually, this works, because it's minimum number of holes for a given maxlabel, but it's unclear)
            memory[0] = [number_of_labels,deepcopy(labels)]
#            print memory[0]
        return False

#TODO? similar checks could optimize for most even distribution of labels, and more


# this method is getting large, so here is what each input does:
# spm- shortest path matrix, for efficient checks
# vertex- the current vertex index
# label- the label to assign to the vertex
# maxlabel- the current maximum label
# labels- the list of labels
# constraints- the constraints on the labeling, for example L(2,1)
# final_check- the method to run on a completed labeling to check whether it meets
#              the whole-graph constraints (no holes, for example)
# memory- memory for use in optimizing labelings (for example, fewest holes)

# should work with reals
def try_label (spm, vertex, label, maxlabel, labels, constraints, final_check, d_set, memory = [None]):
    #return [i for i in xrange(len(labels))]
    #if vertex <= 3:
    #  bar = "-"*vertex
    #  print bar + str(color)
    #yay for verbose output! Make sure not freezing with above code

    # if pre-colored, then called with this as label, so we are not ignoring it.
    labels[vertex] = label
    if not check_vertex_labeling(spm[vertex], vertex, labels, constraints): # only need to pass check_labeling the current row of the SPM.
        return False

    # if we're on the last vertex, then check for holes if we are looking for a no-hole coloring
    if (len(labels)-1 == vertex):
        return final_check(labels, maxlabel, memory)

    if labels[vertex+1] != 'NULL':
        
        if try_label (spm, vertex+1, labels[vertex+1], maxlabel, labels, constraints, final_check, d_set, memory) != False:
            return labels

    else:
        for l in d_set[0:maxlabel+1]: # This is probably not correct if not using L(2,1) labeling because d_set may not be consecutive
            #for example, is d_set is [0, 1,3,4], max label of two, can't try to use three.
#        for l in range(maxlabel+1):   # TODO: improve efficiency here by selecting which colors we can use?  or only useful for going through list in right order?  won't speed up that much...
            if try_label(spm, vertex+1, l, maxlabel, labels, constraints, final_check, d_set, memory) != False:
                return labels
        labels[vertex+1] = 'NULL' # reset vertex labeling so that it is not triggered as a pre-configured one next time through the algorithm

    return False

# #TODO: Optimize for [L(2,1)] labellings, [for example]...even just with constants instead of len(constraints), etc.

# Works with reals
def check_vertex_labeling (sprow, vertex, labels, constraints):
    maxdist = len(constraints) # don't calculate every time!
    for i in range(vertex):
        dist = sprow[i]
        if 0 < dist <= maxdist: # if these two vertices are close enough to matter...
            labdist = abs(labels[i]-labels[vertex]) # the "labeling distance"; separation of the labels
            if labdist < constraints[dist-1]: #checks the coloring constraints to make sure it works
                return False
    return True

# Works with reals
def check_vertex_labeling_no_holes(sprow, vertex, labels, constraints):
    pass

# Works with reals
def build_d_set(constraints, numverts, i=0, setlist=[], addthis=0):
    # I believe this creates a listing of all possible labels that could ever be needed for a graph with numvert verrtices
    myset=set(setlist)
    if i < len(constraints)-1:
        for a in range(numverts):
            myset = build_d_set(constraints, numverts, i+1, myset, addthis+a*constraints[i])
    else:
        for a in range(numverts):
            myset.add(a*constraints[i]+addthis)
    return myset

#adds 2 dimensional matrices of the same size
def matrix_addition(mat1,mat2):
    newmat=[]
    for i in xrange(len(mat1)):
        newmat.append(vector_addition(mat1[i],mat2[i]))
    return newmat
#adds 1 dimensional vectors of the same size
def vector_addition(vec1,vec2):
    newvec=[]
    for i in xrange(len(vec1)):
        newvec.append(vec1[i]+vec2[i])
    return newvec
