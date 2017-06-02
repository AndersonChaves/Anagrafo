import numpy as np
import networkx as nx
from Grafo import Grafo
from ArvoreT import ArvoreT
import math
from Starlike import StarlikeTipo1

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

    def gerar_starlike_como_matriz_de_adjacencias(self, tamanhos_dos_ramos):
        #Quantidade de nos
        n = 1
        for t in tamanhos_dos_ramos:
            n += t
        matriz = np.zeros((n, n))

        #preenchendo valores referentes a vertice de grau maximo
        r = 1
        for t in tamanhos_dos_ramos:
            matriz[0][r] = 1
            matriz[r][0] = 1
            r = r + t

        #preenchendo valores referentes aos ramos
        i = 1
        j = 0
        for t in tamanhos_dos_ramos:
            if t > 1:
                for j in range(i, i+t - 1):
                    matriz[j][j+1] = 1
                    matriz[j+1][j] = 1
            i = i + t
        return matriz

    def gerar_starlike_como_nx(self, tamanhos_dos_ramos):
        return nx.from_numpy_matrix(self.gerar_starlike_como_matriz_de_adjacencias(tamanhos_dos_ramos))

    def gerar_starlike(self, tamanhos_dos_ramos):
        grafo_nx = self.gerar_starlike_como_nx(tamanhos_dos_ramos)
        nome = "T("
        i = 0
        for i in range(len(tamanhos_dos_ramos)):
            nome += str(tamanhos_dos_ramos[i])
            if i < len(tamanhos_dos_ramos)-1:
                nome += ', '
        nome += ')'
        return StarlikeTipo1(nx.Graph(grafo_nx), nome)

    def gerar_lista_de_starlikes_de_mesma_altura_por_numero_de_ramos_e_n_maximo(self, numero_de_ramos, n_maximo):
        lista_de_grafos = []
        l = 1
        n = numero_de_ramos * l + 1
        while n <= n_maximo:
            lista_de_ramos = [l] * numero_de_ramos
            lista_de_grafos.append(self.gerar_starlike(lista_de_ramos))
            l += 1
            n = numero_de_ramos * l + 1
        return lista_de_grafos


