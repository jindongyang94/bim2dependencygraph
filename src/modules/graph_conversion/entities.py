import networkx as nx


class Task:
    """
    This is to encapsulate the needed task in a higher node encapsulation to easily access the information for each construction task
    """
    pass


class WorkFlow(nx.DiGraph):
    """ 
    This is to build the entire worflow made of nodes or tasks, and calculate the higher properties such as critical path etc. 
    """

    def __init__(self):
        super().__init__()
        self._dirty = True
        self._makespan = -1
        self._critical_path = None

    def add_node(self, *args, **kwargs):
        self._dirty = True
        super().add_node(*args, **kwargs)

    def add_nodes_from(self, *args, **kwargs):
        self._dirty = True
        super().add_nodes_from(*args, **kwargs)

    def add_edge(self, *args):  # , **kwargs):
        self._dirty = True
        super().add_edge(*args)  # , **kwargs)

    def add_edges_from(self, *args, **kwargs):
        self._dirty = True
        super().add_edges_from(*args, **kwargs)

    def remove_node(self, *args, **kwargs):
        self._dirty = True
        super().remove_node(*args, **kwargs)

    def remove_nodes_from(self, *args, **kwargs):
        self._dirty = True
        super().remove_nodes_from(*args, **kwargs)

    def remove_edge(self, *args):  # , **kwargs):
        self._dirty = True
        super().remove_edge(*args)  # , **kwargs)

    def remove_edges_from(self, *args, **kwargs):
        self._dirty = True
        super().remove_edges_from(*args, **kwargs)


    ## Sub Functions
    def _forward(self):
        for n in nx.topological_sort(self):
            S = max([self.node[j]['C']
                     for j in self.predecessors(n)], default=0)
            self.add_node(n, S=S, C=S + self.node[n]['p'])

    def _backward(self):
        for n in list(reversed(list(nx.topological_sort(self)))):
            Cp = min([self.node[j]['Sp']
                      for j in self.successors(n)], default=self._makespan)
            self.add_node(n, Sp=Cp - self.node[n]['p'], Cp=Cp)

    def _compute_critical_path(self):
        G = set()
        for n in self:
            if self.node[n]['C'] == self.node[n]['Cp']:
                G.add(n)
        self._critical_path = self.subgraph(G)

    ## Properties
    @property
    def makespan(self):
        if self._dirty:
            self._update()
        return self._makespan

    @property
    def critical_path(self):
        if self._dirty:
            self._update()
        return self._critical_path

    def _update(self):
        self._forward()
        self._makespan = max(nx.get_node_attributes(self, 'C').values())
        self._backward()
        self._compute_critical_path()
        self._dirty = False
    
            

if __name__ == "__main__":
    workflow_example = WorkFlow()
    
    workflow_example.add_node(1, p=5)
    workflow_example.add_node(2, p=6)
    workflow_example.add_node(3, p=9)
    workflow_example.add_node(4, p=12)
    workflow_example.add_node(5, p=7)
    workflow_example.add_node(6, p=12)
    workflow_example.add_node(7, p=10)
    workflow_example.add_node(8, p=6)
    workflow_example.add_node(9, p=10)
    workflow_example.add_node(10, p=9)
    workflow_example.add_node(11, p=7)
    workflow_example.add_node(12, p=8)
    workflow_example.add_node(13, p=7)
    workflow_example.add_node(14, p=5)

    workflow_example.add_edges_from(
        [(1, 2), (2, 4), (4, 7), (7, 10), (10, 12), (12, 14)])
    workflow_example.add_edges_from(
        [(1, 3), (3, 6), (3, 5), (6, 9), (6, 8), (5, 9), (5, 8), (9, 11), (8, 11)])
    workflow_example.add_edges_from([(11, 12), (11, 13), (13, 14)])

    print(workflow_example.makespan)
    print(workflow_example.critical_path.nodes())