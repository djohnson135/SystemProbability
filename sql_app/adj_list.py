import copy


#add probability later but for now lets get into the crux of this problem
class AdjNode:
    def __init__(self, node_id):
        self.vertex = node_id
        self.next = None


class Graph: # add a copy constructor to inherit graphs
    def __init__(self, num, orig=None):
        
        if orig is None:
            self.no_copy_constructor(num)
        else:
            self.copy_constructor(orig)
        
    def no_copy_constructor(self, num):    
        self.V = num
        self.graph = [None] * self.V   
    def copy_constructor(self, orig):
        self.V = copy.deepcopy(orig.V)
        self.graph = copy.deepcopy(orig.graph)
        
    # Add edges
    def add_edge(self, s, d):
        node = AdjNode(d)
        node.next = self.graph[s]
        self.graph[s] = node

        node = AdjNode(s)
        node.next = self.graph[d]
        self.graph[d] = node

    # Print the graph
    def print_agraph(self):
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")
    # @classmethod
    # def from_graph(cls, class_instance):
    #     vertex = copy.deepcopy(class_instance.vertex)
        


# if __name__ == "adj_list":
V = 5

# Create graph and edges
graph = Graph(V)
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(0, 3)
graph.add_edge(1, 2)

graph.print_agraph()

print("\n")
test_copy_graph = Graph(0,graph) # this is ugly but for now lets just keep it this way you need to have a 0 first to copy
test_copy_graph.print_agraph()

graph.add_edge(4,1)
print("added 4, 1 to orig graph\n")
graph.print_agraph()

print("copy graph should not have the added 4 1\n")
test_copy_graph.print_agraph()

def reduce_graph(system):
    
    pass
