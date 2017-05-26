from ExperimentoHeuristicaMacap import ExperimentoHeuristicaMacap
from Grafo import Grafo
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from AlgoritmoHeuristicaDeMenorDiametro import AlgoritmoHeuristicaDeMenorDiametro
import networkx as nx
import numpy as np

if __name__ == "__main__":
    #for i in range(3, 15):
    #G = Grafo(nx.path_graph(3))
    #a = (nx.laplacian_matrix(G.grafo_nx))
    #print a[0]
    #print len(a)
    #print len(a[0])

    L = [[1, 0, -1], [0, 1, -1], [-1, -1, 2]]
    print np.linalg.eig(L)[0]
    print '\n'
    print np.linalg.eig(L)[1]



    #print G.obter_conectividade_algebrica()
    #print AlgoritmoHeuristicaDeForcaBruta().executar_algoritmo(G)
    #print AlgoritmoHeuristicaDeMenorDiametro().executar_algoritmo(G)


#    for i in [10]:
#        experimento = ExperimentoHeuristicaMacap(i, i+2, 2*i)
#        experimento.executar()
#    experimento = ExperimentoComArvoresT()


