# -*- coding:UTF-8 -*-

from Grafo import Grafo

#Classe para grafos Starlike - Grafos que possuem um único vértice de grau máximo,
#e todos os demais de grau dg <= 2 (notação T(n, n, ..., n))

class Starlike(Grafo):
    quantidade_de_caminhos = -1

    def __init__(self, grafo_nx, nome=""):
        Grafo.__init__(self, grafo_nx, nome)
        self.quantidade_de_caminhos = self.obter_grau_maximo()