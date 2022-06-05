import copy

from enum import Enum

class status(Enum):
    BEGIN = 1
    TERMINAL = 2

#add probability later but for now lets get into the crux of this problem
class AdjNode:
    def __init__(self, node_id):
        self.vertex = node_id
        self.next = None


class GraphDict: # add a copy constructor to inherit graphs
    def __init__(self, num, orig=None):
        
        if orig is None:
            self.no_copy_constructor(num)
        else:
            self.copy_constructor(orig)
        
    def no_copy_constructor(self, num):    
        self.V = num
        self.graph = dict()  
    def copy_constructor(self, orig):
        self.V = copy.deepcopy(orig.V)
        self.graph = copy.deepcopy(orig.graph)
        
    # Add edges
    def add_edge(self, s, d):
        dnode = AdjNode(d)
        snode = AdjNode(s)
        
        
        if self.graph.get(s) is None:
            self.graph[s] = list()
        
        if self.graph.get(d) is None:
            self.graph[d] = list()
            
        self.graph[s].append(dnode)
        self.graph[d].append(snode)


    # Print the graph
    def print_agraph(self):
        for k, v in self.graph.items():
            print("Vertex " + str(k) + ":", end="")
            for i in range(len(v)):
                print(" -> {}".format(v[i].vertex), end="")
                # print(v[i].vertex)
                
            print(" \n")
            
    def reduce_graph(self):
    #first check if you can find an element in series. Null or special character needed.
    #to find an element in series we will need to determine if the size of a row in the adjacency list is 1 (not including the vertex)
        # status.TERMINAL
        for i in range(self.V):
            
            pass
            
            
    def Series(self):
        for k, v in self.graph.items():
            
            pass
    # @classmethod
    # def from_graph(cls, class_instance):
    #     vertex = copy.deepcopy(class_instance.vertex)
V = 5

# Create graph and edges
graph = GraphDict(V)
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(0, 3)
graph.add_edge(1, 2)

graph.print_agraph()