#Question 18
from graph import Graph, graph_from_file, min_power_opti
from operator import itemgetter
from tqdm import tqdm

#Première idée : algorithme glouton

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
