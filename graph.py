
import random
import numpy as np
import math
from tqdm import tqdm
from time import perf_counter

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


    def add_edge(self, node1, node2, power_min, dist=1):  # Question 1#
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

# On regarde pour chacun des deux noeuds si ils sont déjà dans le graphes ou non, auquel cas on les ajoute, sinon on rajoute seulement l'arrête

        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)

        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

# On rajoute l'arrête à chaque noeud, la puissance associée et la distance

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1


# Question 2 #

# Fonction qui visite les noeuds

    def components(self, node, nodes_v):
        L = [node]

        for i in self.graph[node]:
            k = i[0]

            if not nodes_v[k]:
                nodes_v[k] = True
                L += Graph.components(self, k, nodes_v)  # On rajoute aux noeud ces composants

        return L


    def connected_components(self):

        A = []  # A contiendra les listes de composantes connectées
        nodes_v = {node: False for node in self.nodes}  # Dictionnaire qui permet de savoir si l'on est déjà passé par un point

        for k in self.nodes:

            if not nodes_v[k]:
                nodes_v[k] = True
                A.append(Graph.components(self, k, nodes_v))

        return A


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component),
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """

        return set(map(frozenset, self.connected_components()))



    def get_path_with_power(self, src, dest, power):  # Question 3 #
        """ Teste s'il existe un chemin possible entre src et dest avec pour puissance associé au camion la puisance power """
        A_examiner = [(src, [src])]
        
        deja_vu = []

        while A_examiner != []:
            sommet, chemin = A_examiner.pop(0)
            deja_vu.append(sommet)

            for voisin in self.graph[sommet]:

                if voisin[0] not in deja_vu:

                    if voisin[1] <= power:

                        if voisin[0] == dest:
                        
                            return chemin+ [voisin[0]]
                            A_examiner = []

                        else:
                            A_examiner.append((voisin[0], chemin+[voisin[0]]))

        return None
                            

    def min_power(self, src, dest):  # Question 6 #
        """
        Should return path, min_power.
        """

        # On procède à une dichotomie en commencant par les puisances de 2 afin d'éviter de tester trop de puissances
        i = 1
        g = Graph.get_path_with_power(self, src, dest, i)

        if g == 0:
            return None

        while g is None:
            i *= 2
            g = Graph.get_path_with_power(self, src, dest, i)

        bas = i/2
        haut = i

        while abs(bas-haut) > 1e-5:
            milieu = math.floor((haut+bas)/2)
            h = Graph.get_path_with_power(self, src, dest, milieu)

            if h is None:
                bas = milieu

            else:
                haut = milieu

            h = Graph.get_path_with_power(self, src, dest, math.floor(haut))

        return [h, math.floor(haut)]


def graph_from_file(filename):  # Question 1 et 4 #
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

        for _ in tqdm(range(m)):
            edge = list(map(int, file.readline().split()))

            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min)  # Si la distance n'est pas précisée, la valeur par défaut est 1

            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)

            else:
                raise Exception("Format incorrect")

    return g


# Question 10 #

def fonction_chrono(filename,  g_ch):

    t = perf_counter()

# Ouverture du fichier et récupération des données

    with open(filename, "r") as file:
        k = map(int, file.readline().split())

# On choisit au hasard un trajet et on applique la fonction, on repète le processus 100 fois pour trouver une valeur moyenne

    for i in tqdm(range(3)):
        a = g_ch.nodes[random.randint(0, len(g_ch.nodes)-1)]
        b = g_ch.nodes[random.randint(0, len(g_ch.nodes)-1)]
        M = g_ch.min_power(a, b)
        L, p = M[0], M[1]

    t_int = perf_counter()
    t_fin = (t_int - t)*(k/3)
    return t_fin


# Question 12 #
    """
    Premiere version de kruskal qui ne fonctionne pas 
    
def Find(x, Parent):

    while x != Parent[x]:
        x = Parent[x]

    return x


def Union(x,y, Parent):
    xracine = Find(x, Parent)
    yracine = Find(y, Parent)

    if xracine != yracine:
        Parent[xracine] = yracine


def kruskal(g):

    L = []  # L correspondra à l'arbre couvrant minimal, avec les noeuds du haut vers le bas par composante connexe
    noeud_deja_vu = {x: False for x in g.nodes}

    for a in tqdm(g.connected_components()): # On applique ce processus à chaque composante connexe
        R = []  
        T = [] # T sera la liste des arrêtes de chacune des composantes connexes

        for i in range(len(a)):
            b = a[i]

            for j in g.graph[b]:
                (u,v,w) = j

                if j not in(R) and not(noeud_deja_vu[j[0]]):
                    T.append((b, j[0], j[1]))
                    R.append(j)

            noeud_deja_vu[b] = True

         # Maintenant on a la liste des arrêtes sous la forme (noeud1,noeud2,puissance), ce qui va nous servir pour l'Union-Find : T
         # Sinon on aurait juste pu ouvrir le fichier et parcourir les arrêtes.

        N = len(T)

        if N >1:

            for n in range(1,N): # On trie les arrêtes par ordre croissant
                cle = T[n]
                j = n-1

                while j>=0 and T[j][2] > cle[2]:
                    T[j+1] = T[j]
                    j = j-1

                T[j+1] = cle

        # On va maintenant se servir de l'Union-Find pour déterminer si l'arrête ajoutée crée un cycle ou pas 

        Parent = {x: x for x in g.nodes}

        for a in T:
            u, v = a[0], a[1]

            if Find(u, Parent) != Find(v, Parent):
                L.append(a)
                Union(u,v, Parent)

    n = len(L)
    k, j = str(n+1), str(n)
    g_mst = Graph()

    for i in L:
        g_mst.add_edge(i[0], i[1], i[2])

    return [g_mst, Parent]

# Nous rencontrons encore des difficultés à terminer l'Union-Find de façon fonctionnelle
    """
    
def kruskal(g):
    Deja_vu = {} 

    arretes = []

    for node_a in g.nodes:

        for arrete in g.graph[node_a]: 

            node_b, p, d = arrete

            if not ((node_a, node_b) in Deja_vu):

                Deja_vu[(node_a, node_b)] = True

                Deja_vu[(node_b, node_a)] = True 

                arretes.append((node_a, node_b, p, d))
        
    arretes.sort(key= lambda a : a[2]) # on trie les arretes par puissance croissante
    

    # On construit l'arbre

    g_mst = Graph(g.nodes)

    arbre_connecter = {n: [n] for n in g_mst.nodes} # on identifie avec qui est connecté n 

        
    for arrete in arretes:

        
        node_a, node_b, p, d = arrete

        if not (arbre_connecter[node_b][0] == arbre_connecter[node_a][0]):

            g_mst.add_edge(node_a, node_b, p, d)

            for node_c in arbre_connecter[node_b]: # on fusionne les deux arbres

                arbre_connecter[node_a].append(node_c)

                arbre_connecter[node_c] = arbre_connecter[node_a] 
                               
    return g_mst






# Question 13 #

g = graph_from_file('input/network.05.in')
print(kruskal(g))


# Question 14 #

def min_power_opti(g ,t):
    src, dest = t[0], t[1]
    g_mst = kruskal(g)
    p_min = 0
    A_examiner = [(src, [src])]
    chemins = []
    deja_vu = []
    power = np.inf

    while A_examiner != []:

        sommet, chemin = A_examiner.pop(0)

        deja_vu.append(sommet)

        for voisin in g_mst.graph[sommet]:

            if voisin[0] not in deja_vu:

                if voisin[1] <= power:

                    if voisin[0] == dest:
                        chemins.append(chemin + [voisin[0]])
                        for i in range(len(chemins[0])-1):

                            for voisin1 in g.graph[chemins[0][i]]:

                                if voisin1[0] == chemins[0][i+1]:

                                    if voisin1[1] > p_min:

                                        p_min = voisin1[1]
                        
                        return p_min
                        A_examiner = []

                    else:
                        A_examiner.append((voisin[0], chemin+[voisin[0]]))
    print(p_min)
    return None
    


# Question 15 #

def fonction_chrono_opti(filename,  g_ch):

    t = perf_counter()

# Ouverture du fichier et récupération des données

    with open(filename, "r") as file:
        k = map(int, file.readline().split())

# On choisit au hasard un trajet et on applique la fonction, on repète le processus 100 fois pour trouver une valeur moyenne

    for i in range(100):
        a = g_ch.nodes[random.randint(0, len(g_ch.nodes)-1)]
        b = g_ch.nodes[random.randint(0, len(g_ch.nodes)-1)]
        [M, N] = min_power_opti(g, [a,b])[0]

        if [M, N] == None:
            return None
        
        L, p = M[0], M[1]

    t_int = perf_counter()
    t_fin = (t_int - t)*(k/100)
    return t_fin


#Question 18
from graph import Graph, graph_from_file, min_power_opti
from operator import itemgetter
from tqdm import tqdm

#Première idée : algorithme glouton
def maximisation_profit():
    # On commence par associer à chaque trajet le profit rapporté 
    g_18 = graph_from_file('input/network.1.in')


    with open('input/routes.1.in', "r") as file:

        L = []
        [n] = list(map(int, file.readline().split()))
        
        

        for _ in range(n):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                src, dst, util = edge
                L.append(((src,dst),util))
            if len(edge) == 4:
                src, dst, util, l = edge
                L.append(((src,dst),util))

        # L est la liste des trajets et de l'utilité associée


        h = open('input/trucks.0.in', 'r')
        C = []
        [m] = list(map(int, h.readline().split()))

        for _ in range(m):
            edge = list(map(int, h.readline().split()))
            if len(edge) == 2:
                power, cout = edge
                C.append((power, cout))
            if len(edge) == 3:
                power, cout, l = edge
                C.append((power, cout))

        # C est la liste de la puissance et des couts

        '''for each trajet 
        on cherche la puissance min necessaire
        on cherche le camion le moins cher avec au moins cette puissance et on l'ajoute
        on se retrouvera avec une liste de tuples (trajet, utilite, cout)
        profit = utilite - cout
        liste de tuples (trajet, utilite, cout, profit)'''

        L_Sort = sorted(L, key=itemgetter(1), reverse=True)
        
        # On trie les trajets par ordre décroissant d'utilité

        C_Sort = sorted(C, key=itemgetter(0,1))
        # On trie les camions par ordre croissant de puissance puis par ordre croissant de coût
        
        B = 25*(10**9)
        # B est le budget de l'entreprise

        R = []
        # R sera la liste des camions à acheter associés à leur trajet respectif

        Pi = 0
        # Pi sera le profit total

        for i in tqdm(range(len(L_Sort))):
            puis = min_power_opti(g_18, L_Sort[i][0])
            if puis == None:
                continue
            J = []
            while J == []:
                for j in range(len(C_Sort)):
                
                    if C_Sort[j][0] >= puis:
                        
                        A = list(C_Sort[j:len(C_Sort)])
                        A = sorted(A, key=itemgetter(1))

                        J.append(A[0])
                        if J[0][1] <= B:
                            B = B - J[0][1]
                            R.append((L_Sort[i][0], C_Sort[j]))
                            Pi += L_Sort[i][1] - J[0][1]
        

        print('La liste des camions à acheter est : ', R,'\n Le profit total ainsi réalisé par l\'entreprise sera de', Pi, 'et son budget restant sera de', B)
