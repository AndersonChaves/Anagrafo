import numpy as np
import networkx as nx
from Grafo import Grafo
from ArvoreT import ArvoreT
import math


class GeradorDeGrafos():

    def gerar_arvore_t_como_matriz_de_adjacencias(self, k, l, diametro):
        m = k + l + (diametro - 1)
        n = m
        matriz = np.zeros((m, m))

        id_no_pai1 = (k + 1) - 1
        id_no_pai2 = (k + diametro - 1) - 1

        for i in range(m):
            for j in range(n):
                if i < id_no_pai1:
                    if j == id_no_pai1:
                        matriz[i][j] = 1

                elif i == id_no_pai1:
                    if j < id_no_pai1 or j == id_no_pai1 + 1:
                        matriz[i][j] = 1

                elif i == id_no_pai2:
                    if j > id_no_pai2 or j == id_no_pai2 - 1:
                        matriz[i][j] = 1

                elif i > id_no_pai2:
                    if j == id_no_pai2:
                        matriz[i][j] = 1

        for i in range(id_no_pai1, id_no_pai2):
            matriz[i + 1][i] = 1
            matriz[i][i + 1] = 1
        return matriz

    def gerar_arvore_t_como_nx(self, k, l, diametro):
        return nx.from_numpy_matrix(self.gerar_arvore_t_como_matriz_de_adjacencias(k, l, diametro))

    def gerar_arvore_t(self, k, l, diametro, nome=""):
        grafo_nx = self.gerar_arvore_t_como_nx(k, l, diametro)
        return ArvoreT(nx.Graph(grafo_nx), diametro, grafo_nx.order(), k, l, nome)

    def gerar_broom(self, diametro, n, nome=""):
        k = 1
        l = n-diametro
        if nome == "":
            nome_do_grafo = "T(" + str(n) + ", " + str(diametro) + ", " + str(k) + ")"
        return self.gerar_arvore_t(k, l, diametro, nome)

    def gerar_arvores_t_por_ordem_e_diametro(self, ordem, diametro):
        lista_de_grafos = []
        nos_nao_folha = ordem - (diametro - 1)
        k_maximo = math.floor( nos_nao_folha / 2 )
        for k in range(1, int(k_maximo + 1)):
            l = ordem - (diametro - 1) - k
            nome_do_grafo = "T(" + str(ordem) + ", " + str(diametro) + ", " + str(k) + ")"
            arvore_t = self.gerar_arvore_t(k, l, diametro, nome_do_grafo)
            lista_de_grafos.append(arvore_t)
        return lista_de_grafos


    def gerar_listas_de_arvores_t_por_diametro_variando_ordem(self, *args):
        if len(args) == 3:
            ordem_minima, ordem_maxima, diametro = args
        elif len(args) == 2:
            ordem_maxima, diametro = args
            ordem_minima = diametro + 1
        else:
            raise TypeError("Numero incorreto de argumentos.")

        print "Gerando grafos de diametro " + str(diametro)
        lista_de_grafos = []
        for ordem in range(ordem_minima, ordem_maxima + 1):
            print "Gerando grafos de ordem " + str(ordem)
            lista_de_grafos.append(self.gerar_arvores_t_por_ordem_e_diametro(ordem, diametro))
        return lista_de_grafos

    def gerar_listas_de_arvores_t_por_diametro_variando_ordem_com_k_fixado(self, ordem_maxima, diametro, k, ordem_minima = 0):
        if ordem_minima == 0:
            ordem_minima = diametro + 1
        print "Gerando grafos de diametro " + str(diametro)
        lista_de_grafos = []
        for ordem in range(ordem_minima, ordem_maxima + 1):
            print "Gerando grafos de ordem " + str(ordem)
            l = (ordem - k - (diametro - 1))
            nome_do_grafo = "T(" + str(ordem) + ", " + str(diametro) + ", " + str(k) + ")"
            lista_de_grafos.append(self.gerar_arvore_t(k, l, diametro, nome_do_grafo))
        return lista_de_grafos

    def gerar_caminho(self, n, nome = ""):
        if nome == "":
            nome = 'Caminho(' + str(n) + ')'
        return Grafo(nx.path_graph(n), nome)


'''
Exemplo:
    matrizDeAdjacencias = np.array([[0, 0, 1, 0, 0, 0, 0],  #
                                    [0, 0, 1, 0, 0, 0, 0],  # '<---K = 2'
                                    [1, 1, 0, 1, 0, 0, 0],  #
                                    [0, 0, 1, 0, 1, 1, 1],  #
                                    [0, 0, 0, 1, 0, 0, 0],  # '<--K + diam'
                                    [0, 0, 0, 1, 0, 0, 0],  #
                                    [0, 0, 0, 1, 0, 0, 0]])  #
'''

'''import numpy.linalg as linalg


A = np.asmatrix([[2, 0], [0, 4]])
print "A = "
print A

D = np.asmatrix([[2, 3], [1, 3]])
print "D = "
print D


Dinv = linalg.inv(D)
print "D^-1 = "
print Dinv


B  = Dinv * A * D
print "B = D^-1 * A * D = "
print B


print "autovalores, autovetores de A:"
print linalg.eig(A)

print "autovalores, autovetores de B:"
print linalg.eig(B)

'''