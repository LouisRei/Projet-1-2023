import numpy

import math



class Graph:

    """

    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 

    Attributes: 

    -----------

    nodes: NodeType

        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.

        We will usually use a list of integers 1, ..., n.

    graph: dict

        A dictionnary that contains the adjacency list of each node in the form

        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]

        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge

    nb_nodes: int

        The number of nodes.

    nb_edges: int

        The number of edges. 

    """



    def __init__(self, nodes=[]):

        """

        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 

        -----------

        nodes: list, optional

            A list of nodes. Default is empty.

        """

        self.nodes = nodes

        self.graph = dict([(n, []) for n in nodes])

        self.nb_nodes = len(nodes)

        self.nb_edges = 0

    



    def __str__(self):

        """Prints the graph as a list of neighbors for each node (one per line)"""

        if not self.graph:

            output = "The graph is empty"            

        else:

            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"

            for source, destination in self.graph.items():

                output += f"{source}-->{destination}\n"

        return output

    

    def add_edge(self, node1, node2, power_min, dist=1):

        """

        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 



        Parameters: 

        -----------

        node1: NodeType

            First end (node) of the edge

        node2: NodeType

            Second end (node) of the edge

        power_min: numeric (int or float)

            Minimum power on this edge

        dist: numeric (int or float), optional

            Distance between node1 and node2 on the edge. Default is 1.

        """

        if node1 not in self.graph:

            self.graph[node1] = []

            self.nb_nodes += 1

            self.nodes.append(node1)

        if node2 not in self.graph:

            self.graph[node2] = []

            self.nb_nodes += 1

            self.nodes.append(node2)



        self.graph[node1].append((node2, power_min, dist))

        self.graph[node2].append((node1, power_min, dist))

        self.nb_edges += 1

    



    def get_path_with_power(self, src, dest, power):

        (u, v) = (src, dest)  # u et v sont deux chiffres qui representent un noeud

        a = 0

        # Si les deux villes u et v ne sont pas dans une même composante connexe on renvoit 'None'

        for i in Graph.connected_components_set(self):

            if u not in i or v not in i:

                a +=1

        if a == len(Graph.connected_components_set(self)):

            return None



        # Donc les deux villes sont dans une même composante, maintenant on va étudier tous les chemins



        precedent = {x: None for x in self.nodes}

        Deja_traite = {x: False for x in self.nodes}

        distance = {x: float('inf') for x in self.nodes}

        distance[u] = 0

        A_traiter = [(distance[u], u)]

        while A_traiter:

            dist_noeud, noeud = A_traiter.pop()

            if not Deja_traite[noeud]:

                Deja_traite[noeud] = True

                for (voisin, p_min, d) in self.graph[noeud]:

                    dist_voisin = dist_noeud + d

                    if power >= p_min:

                        if dist_voisin < distance[voisin]:

                            distance[voisin] = dist_voisin

                            precedent[voisin] = noeud

                            A_traiter.append((dist_voisin, voisin))



            A_traiter.sort(reverse=True)

        l = len(precedent)

        L = [v]

        

        a = precedent[v]

        for i in range(len(precedent)):

            L.append(a)

            

            if a == u:

                break

            if a == None:

                return None

            a = precedent[a]

        M = []

        for i in range(len(L)):

            M.append(L[-i-1])

        return M

    



    def connected_components(self):

        A = []  # listes vides qui contiendra les listes de composants connectés



        nodes_v = {node: False for node in self.nodes}  # dictionnaire qui permet de savoir si l'on est déjà passé par un point



        def components(node):



            L = [node]

            for i in self.graph[node]:

                k = i[0]

                if not nodes_v[k]:

                    nodes_v[k] = True

                    L += components(k)  # on rajoute aux noeud ces composants



            return L



        for k in self.nodes:

            if not nodes_v[k]:

                A.append(components(k))



        return A







    def connected_components_set(self):

        """

        The result should be a set of frozensets (one per component), 

        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}

        """

        return set(map(frozenset, self.connected_components()))

    

    def min_power(self, src, dest):

        """

        Should return path, min_power. 

        """

        j = 0

        i = 2**j

        g = Graph.get_path_with_power(self, src, dest, i)



        while g is None:

            j += 1

            g = Graph.get_path_with_power(self, src, dest, i)



        bas = 2**(j-1)

        haut = i



        while abs(bas-haut) > 1:

            milieu = math.floor((haut+bas)/2)

            h = Graph.get_path_with_power(self, src, dest, milieu)

            if h is None:

                bas = milieu

            else:

                haut = milieu



        return (math.floor(milieu), h[0])





def graph_from_file(filename):

    """

    Reads a text file and returns the graph as an object of the Graph class.



    The file should have the following format: 

        The first line of the file is 'n m'

        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)

        The nodes (node1, node2) should be named 1..n

        All values are integers.



    Parameters: 

    -----------

    filename: str

        The name of the file



    Outputs: 

    -----------

    g: Graph

        An object of the class Graph with the graph from file_name.

    """

    with open(filename, "r") as file:

        n, m = map(int, file.readline().split())

        g = Graph(range(1, n+1))

        for _ in range(m):

            edge = list(map(int, file.readline().split()))

            if len(edge) == 3:

                node1, node2, power_min = edge

                g.add_edge(node1, node2, power_min) # will add dist=1 by default

            elif len(edge) == 4:

                node1, node2, power_min, dist = edge

                g.add_edge(node1, node2, power_min, dist)

            else:

                raise Exception("Format incorrect")

    return g