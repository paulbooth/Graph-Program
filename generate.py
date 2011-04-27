#!/usr/bin/python
from graph import *
from math import *
import tkSimpleDialog
import tkMessageBox

def generate(type, options):
    if type == "petersen":
        return petersen(options)
    elif type == "star":
        return star(options)
    elif type == "cycle":
        return cycle(options)
    elif type == "grid":
        return grid(options)
    elif type == "mobius":
        return mobius(options)
    elif type == "triangles":
        return triangles(options)
    elif type == "hexagons":
        return hexagons(options)
    elif type == "partite":
        return partite(options)
    return ("ERROR","No graph of this type can be created")
        
def petersen(options):
    num_verts = options[0]
    num_layers = options[1]
    
    if num_verts < 3:
        return ("ERROR", "Must be at least 3 vertices in each layer")
    
    layers = [ [num_verts, [1], 0, num_verts, [1]] for i in range(num_layers)]
    cross_connections = []
    for i in range(num_layers-1):
        cross_connections.append([[num_verts,[0]]] + [[ 0, []] for j in range(num_layers-2-i)])
            
    size = 200
    return circular_graph(layers, cross_connections, size)
    
def cycle(options):
    num_verts = options[0]
    num_layers = options[1]
    
    if num_verts < 3:
        return ("ERROR", "Must be at least 3 vertices in each cycle")
    
    layers = [ [num_verts, [1], 0, num_verts, [1]] for i in range(num_layers)]
    cross_connections = []
    for i in range(num_layers-1):
        cross_connections.append([[ 0, []] for j in range(num_layers-1-i)])
            
    size = 200
    return circular_graph(layers, cross_connections, size)
    
def star(options):
    num = options[0]
    skip = options[1]
    
    if num < 3:
        return ("ERROR", "Must be at least 3 vertices in each cycle")
    
    if not relatively_prime(num, skip):
        return ("ERROR", "Parameters must be relatively prime for a valid star.")

    layer1 = [ num, [1], 0, num, [skip] ]
    layer2 = [ num, [1], 0, num, [1] ]
    layers = [ layer1, layer2 ]
    cross_connections = [[[ num, [0] ]]]
    size = 200
    return circular_graph(layers, cross_connections, size)

def grid(options):
    rows = options[0]
    columns = options[1]
    layers = [ [columns, [1 for i in range(columns-1)] + [0], 0, columns-1, [1]] for i in range(rows)]
    cross_connections = []
    for i in range(rows-1):
        cross_connections.append([[columns,[0]]] + [[ 0, []] for j in range(rows-2-i)])
    
    if rows >= columns:
        ysize = 200
        xsize = 200 * float(columns-1)/(rows-1)
        # print xsize
    else:
        xsize = 200
        ysize = 200 * float(rows-1)/(columns-1)
        # print ysize
    
    return rectangular_graph(layers, cross_connections, xsize, ysize)

def triangles(options):
    rows = options[0]
    columns = options[1]
    wrap=options[2]
    layers = [ [columns, [1 for i in range(columns-1)] + [0], 0, columns-1+(int(wrap>1)), [1]] for i in range(rows)]
    cross_connections = []
    for i in range(rows-1):
        cross_connections.append([[columns*2-1+(int(wrap>1)),[0]*columns+[1]*(columns-1+(int(wrap>1)))]] + [[ 0, []] for j in range(rows-2-i)])
    if wrap>2:
        cross_connections[0]=[[columns*2,[0]*columns+[1]*(columns)]] + [[ 0, []] for j in range(rows-3)]+[[columns*2,[0]*columns+[columns-1]*(columns)]]
    if rows >= columns:
        ysize = 300
        xsize = 300 * float(columns-1)/(rows-1)
        # print xsize
    else:
        xsize = 300
        ysize = 300 * float(rows-1)/(columns-1)
        # print ysize
    
    return rectangular_graph(layers, cross_connections, xsize, ysize)

def partite(options):
    sizes=options[0]
    vertices=[]
    edges=[]
    vertspace=300/max(sizes+[len(sizes)])
    for i in xrange(len(sizes)):
        for s in xrange(sizes[i]):
            vertices.append((vertspace*s,vertspace*i));
    cumsize=0
    for i in xrange(len(sizes)-1):
        for s in xrange(sizes[i]):
            cumjsize=cumsize+sizes[i]
            for j in xrange(i+1,len(sizes)):
                for js in xrange(sizes[j]):
                    edges.append((vertices[cumsize+s],vertices[js+cumjsize]))
                cumjsize+=sizes[j]
        cumsize+=sizes[i]
        
    return (vertices,edges)
    

def hexagons(options):
    rows = options[0]
    columns = options[1]
##    open=2-options[2]
    wrap=options[2]
    layers = [[columns*2, [1 for i in range(2*columns-1)] + [0], 0, 2*columns-1+(int(wrap>1)), [1]] for i in range(rows)]
    cross_connections = []
    for i in range(rows-1):
        cross_connections.append([[columns,[1,-1]]] + [[ 0, []] for j in range(rows-2-i)])
    if wrap>2:
        cross_connections[0]=[[columns,[1,-1]]] + [[ 0, []] for j in range(rows-3)]+[[columns,[-1,columns*2-1]]]
    if rows >= columns:
        ysize = 300
        xsize = 300 * float(columns-1)/(rows-1)
        # print xsize
    else:
        xsize = 300
        ysize = 300 * float(rows-1)/(columns-1)
        # print ysize
    
    return rectangular_graph(layers, cross_connections, xsize, ysize)

def mobius(options):
    n = options[0]
    layer1 = [ (n-1)/2, [1], .5, (n-1)/2 - 1, [1]]
    layer2 = [ (n-1)/2, [1], .5, 0, [1]]
    layer3 = [ (n+1)/2, [1 for i in range((n-1)/2)] + [0], 0, 1, [(n-1)/2]]
    layer4 = [ (n+1)/2, [1 for i in range((n-1)/2)] + [0], 0, (n+1)/2 - 1, [1]]
    layers = [layer1, layer2, layer3, layer4]
    
    cc1 = [[(n-1)/2, [0]],[0, []],[2, [(n-1)/2] + [-1 for i in range((n-5)/2)] + [2] ]]
    cc2 = [[n-1, [0 for i in range((n-1)/2)] + [2 for i in range((n-1)/2)]],[0, []]]
    cc3 = [[(n+1)/2, [0]]]
    
    cross_connections = [cc1, cc2, cc3]
    
    xsize = 200
    ysize = 600/((n-1)/2)
    
    return rectangular_graph(layers, cross_connections, xsize,ysize)
    
def circular_graph(layers, cross_connections, size):
    # this function makes use of pattern lists, which are formatted as follows:
    #
    # layers is a list with one entry for each layer. The layer entry should be formatted as follows:
    # # [number of vertices, vertex spacing pattern, rotation, number of connections, connection pattern]
    # # rotation is in the same scale as the spacing pattern, so if the vertices are evenly spaced
    # # with the pattern [1], then a rotation of .5 will rotate by 1/2 the vertex distance
    #
    # cross connections is a list with an entry for each layer. Each entry should be formatted as follows:
    # # the list contains an entry for each layer further out than the current one, which looks like:
    # # [number of edges, edge spacing pattern]
    # # the pattern will loop continuously until all the edges have been placed. The pattern begins with
    # # the first vertex (usually the top vertex, or the one to the right of the top) and is coded with the
    # # number of vertices to skip from the current position on the target layer
    #
    # size is the radius of the outermost layer
    #
    # patterns are lists that can repeat. If you want an even pattern, a single entry list is sufficient.
    #   if the pattern never repeats, then the list must be as long as the feature being patterned.
    #

    # errors
    # TODO: test error conditions!
    if size <= len( layers ):
        return ("ERROR","too many layers in too little space")
    if (len(layers) != len(cross_connections) + 1) and len(layers) != 1:
        return ("ERROR","number of layers and number of connections don't match")

    layer_sizes = range( size/len(layers), size+1, size/len(layers) ) # radius of each layer

    # place the vertices
    #vertices = [-1] * len(layers)
    vertices = []
    edges = []
    total_verts = 0 # vertices before adding current layer
    for layer in range( len(layers) ):

        curr_layer = layers[layer]      # current layer data
        number_of_vertices = curr_layer[0]
        vertex_spacing_pattern = curr_layer[1]
        spacing_length = len(curr_layer[1])
        init_rotation = curr_layer[2]
        number_of_connections = curr_layer[3]
        connection_pattern = curr_layer[4]
        pattern_length = len(connection_pattern)

        scale = 0.0
        for x in range( number_of_vertices ): # scaling factor
            scale = scale + vertex_spacing_pattern[ x % len( vertex_spacing_pattern ) ]

        rotation = float(init_rotation) / scale        # starting rotation; 1 is a full rotation.

        #vertices[layer] = [-1] * number_of_vertices
        for vertex in range( number_of_vertices ):    # place vertices
            vertices.append(rotate(layer_sizes[layer], rotation))
            rotation = rotation + float(vertex_spacing_pattern[vertex % spacing_length])/scale
        current_location = 0
        for connection in range( number_of_connections ): # place in-layer edges
            # The next two lines allow a "-1" to mean "no connection"
            while connection_pattern[ current_location % pattern_length ] == -1 :
               current_location = current_location + 1
            target_location = (current_location + connection_pattern[ current_location % pattern_length ]) % number_of_vertices
            target_vertex = vertices[total_verts + target_location]
            # TODO: test error conditions!
            if target_location == current_location:
                return ("ERROR", "pattern error, vertex connects to itself")
            for edge in edges:
                current_vertex = vertices[total_verts + current_location % number_of_vertices]
                if (edge[0] in [current_vertex, target_vertex]) and (edge[1] in [current_vertex,target_vertex]):
                    return("ERROR","pattern error, edge already exists")
            edges.append((vertices[total_verts+current_location % number_of_vertices],vertices[total_verts+target_location]))
            current_location = current_location + 1
        
        total_verts += number_of_vertices

    # place cross-layer edges
    total_verts = 0
    for layer in range( len(layers)-1 ):  # start with the inner layer
        layer_connections = cross_connections[layer]
        number_of_base_vertices = layers[layer][0]
        total_target_verts = total_verts+number_of_base_vertices
        for target_layer in range( layer + 1, len(layers) ): # connect to each successive layer out
            curr_target_layer = layer_connections[ target_layer - layer - 1 ]
            number_of_connections = curr_target_layer[0]
            connection_pattern = curr_target_layer[1]
            pattern_length = len(connection_pattern)
            number_of_target_vertices = layers[target_layer][0]
            current_location = 0
            for connection in range( number_of_connections ): #place edges
                while connection_pattern[ current_location % pattern_length ] == -1 :
                    current_location = current_location + 1
                target_location = (current_location + connection_pattern[ current_location % pattern_length ]) % number_of_target_vertices
                target_vertex = vertices[total_target_verts + target_location]
                # TODO: test error conditions!
                for edge in edges: # make sure they aren't duplicated
                    current_vertex = vertices[total_verts + current_location % number_of_base_vertices]
                    if (edge[0] in [current_vertex, target_vertex]) and (edge[1] in [current_vertex,target_vertex]):
                        return("ERROR","pattern error, edge already exists")
                edges.append((vertices[total_verts+current_location % number_of_base_vertices],vertices[total_target_verts+target_location]))
                current_location = current_location + 1
            total_target_verts += number_of_target_vertices
        total_verts += number_of_base_vertices
    return(vertices,edges)

def rectangular_graph(layers, cross_connections, xsize, ysize):
    # this function makes use of pattern lists, which are formatted as follows:
    #
    # layers is a list with one entry for each layer. The layer entry should be formatted as follows:
    # # [number of vertices, vertex spacing pattern, rotation, number of connections, connection pattern]
    # # rotation is in the same scale as the spacing pattern, so if the vertices are evenly spaced
    # # with the pattern [1], then a rotation of .5 will rotate by 1/2 the vertex distance
    #
    # cross connections is a list with an entry for each layer. Each entry should be formatted as follows:
    # # the list contains an entry for each layer further out than the current one, which looks like:
    # # [number of edges, edge spacing pattern]
    # # the pattern will loop continuously until all the edges have been placed. The pattern begins with
    # # the first vertex (usually the top vertex, or the one to the right of the top) and is coded with the
    # # number of vertices to skip from the current position on the target layer
    #
    # size is the radius of the outermost layer
    #
    # patterns are lists that can repeat. If you want an even pattern, a single entry list is sufficient.
    #   if the pattern never repeats, then the list must be as long as the feature being patterned.
    #

    # errors
    # TODO: test error conditions! THESE SHOULD BE CONFORMED TO NEW ERROR SYSTEM!
    if ysize <= len( layers ):
        return ("ERROR","too many layers in too little space")
    if (len(layers) != len(cross_connections) + 1) and len(layers) != 1:
        return ("ERROR","number of layers and number of connections don't match")

    layer_sizes = range( 0, ysize+1, ysize/(len(layers)-1) ) # radius of each layer

    # place the vertices
    #vertices = [-1] * len(layers)
    vertices = []
    edges = []
    total_verts = 0 # vertices before adding current layer
    for layer in range( len(layers) ):

        curr_layer = layers[layer]      # current layer data
        number_of_vertices = curr_layer[0]
        vertex_spacing_pattern = curr_layer[1]
        spacing_length = len(curr_layer[1])
        init_rotation = curr_layer[2]
        number_of_connections = curr_layer[3]
        connection_pattern = curr_layer[4]
        pattern_length = len(connection_pattern)

        scale = 0.0
        for x in range( number_of_vertices ): # scaling factor
            scale = scale + vertex_spacing_pattern[ x % spacing_length ]

        rotation = float(init_rotation) / scale        # starting rotation; 1 is a full rotation.

        #vertices[layer] = [-1] * number_of_vertices
        for vertex in range( number_of_vertices ):    # place vertices
            vertices.append(( rotation*xsize, layer_sizes[layer]))
            rotation = rotation + float(vertex_spacing_pattern[vertex % spacing_length])/scale
        current_location = 0
        for connection in range( number_of_connections ): # place in-layer edges
            # The next two lines allow a "-1" to mean "no connection"
            while connection_pattern[ current_location % pattern_length ] == -1 :
               current_location = current_location + 1
            target_location = (current_location + connection_pattern[ current_location % pattern_length ]) % number_of_vertices
            target_vertex = vertices[total_verts + target_location]
            # TODO: test error conditions!
            if target_location == current_location:
                return ("ERROR", "pattern error, vertex connects to itself")
            for edge in edges:
                current_vertex = vertices[total_verts + current_location % number_of_vertices]
                if (edge[0] in [current_vertex, target_vertex]) and (edge[1] in [current_vertex,target_vertex]):
                    return("ERROR","pattern error, edge already exists")
            edges.append((vertices[total_verts+current_location % number_of_vertices],vertices[total_verts+target_location]))
            current_location = current_location + 1
        
        total_verts += number_of_vertices

    # place cross-layer edges
    total_verts = 0
    for layer in range( len(layers)-1 ):  # start with the inner layer
        layer_connections = cross_connections[layer]
        number_of_base_vertices = layers[layer][0]
        total_target_verts = total_verts+number_of_base_vertices
        for target_layer in range( layer + 1, len(layers) ): # connect to each successive layer out
            curr_target_layer = layer_connections[ target_layer - layer - 1 ]
            number_of_connections = curr_target_layer[0]
            connection_pattern = curr_target_layer[1]
            pattern_length = len(connection_pattern)
            number_of_target_vertices = layers[target_layer][0]
            current_location = 0
            for connection in range( number_of_connections ): #place edges
                while connection_pattern[ current_location % pattern_length ] == -1 :
                    current_location = current_location + 1
                target_location = (current_location + connection_pattern[ current_location % pattern_length ]) % number_of_target_vertices
                target_vertex = vertices[total_target_verts + target_location]
                # TODO: test error conditions!
                for edge in edges: # make sure they aren't duplicated
                    current_vertex = vertices[total_verts + current_location % number_of_base_vertices]
                    if (edge[0] in [current_vertex, target_vertex]) and (edge[1] in [current_vertex,target_vertex]):
                        return("ERROR","pattern error, edge already exists")
                edges.append((vertices[total_verts+current_location % number_of_base_vertices],vertices[total_target_verts+target_location]))
                current_location = current_location + 1
            total_target_verts += number_of_target_vertices
        total_verts += number_of_base_vertices
    return(vertices,edges)    
    
def rotate(radius, rotation):
    # 1 rotation is a full circle
    x = radius * cos(2*pi*rotation)
    y = - radius * sin(2*pi*rotation)
    return (x, y)

def relatively_prime(a, b):
    for i in range(2,min([a,b])+1):
        if a%i==b%i==0:
            return False
    return True
