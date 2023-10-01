from graph import Graph, graph_from_file, kruskal, fonction_chrono
from graph import fonction_chrono_opti, min_power_opti, maximisation_profit
import numpy as np




data_path = "input/"
file_name = "network.2.in"

#g = graph_from_file(data_path + file_name)
# print(g)

# print(Graph.connected_components(g))

#print(Graph.get_path_with_power(g, 1, 36866, 1000000))

# print(kruskal(g)) # Ici trop long -) donc ça joue sur min_opti qui joue sur le chrono

# print(min_power_opti(g, [1, 36866]))

# Test de la fonction et du temps nécessaire Q10

def temps_chemin(x):
    g_ch = graph_from_file('input/network.'+str(x)+'.in')
    route = 'input/routes.'+str(x)+'.in'
    print(fonction_chrono(route,g_ch))

print(temps_chemin(1))


# Question 13 #
"""
g = graph_from_file('input/network.04.in')
print(kruskal(g))
"""

# Question 14 
g = graph_from_file('input/network.2.in')
# g_mst = kruskal(g)
#print(g_mst)
#print(g_mst.get_path_with_power(1, 36866,np.inf))
#print(min_power_opti(g, [1,36866]))

# Question 15 #
"""
g_ch = graph_from_file('input/network.2.in')
route = 'input/routes.'+str(2)+'.in'
print(fonction_chrono_opti(route, g_ch))
"""



"""
route = 'input/routes.'+str(1)+'.in'
print(route)
"""