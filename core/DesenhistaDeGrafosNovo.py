# -*- coding: UTF-8 -*-
import networkx as nx
import matplotlib.pyplot as plt

class DesenhistaDeGrafos:
    tamanhos_de_fonte = [16, 12, 9]
    tamanhos_dos_nos = [1500, 400, 100]
    cores_de_vertices = ['r', 'b']
    arestas_a_destacar = {}
    particionamento_de_vertices = []
    grafo = None
    posicionamento = None
    rotulos = []

    def __init__(self, grafo, cores_de_vertices=()):
        self.grafo = grafo
        self.grafo_nx = grafo.grafo_nx
        self.posicionamento = nx.circular_layout(self.grafo.grafo_nx, scale=0.5)
        if cores_de_vertices != ():
            self.cores_de_vertices = cores_de_vertices
        self.figura = plt.figure()
        self.particionamento_de_vertices = [self.grafo.obter_lista_de_vertices()]

    def efetuar_particionamento_espectral(self):
        print "Efetuando particionamento espectral de grafo " + self.grafo.obter_nome()
        self.cores_de_vertices = ['r', 'b']
        self.particionamento_de_vertices = self.grafo.obter_particionamento_pelo_vetor_fiedler()
        self.rotulos = self.grafo.obter_vetor_fiedler()

    def efetuar_particionamento_isoperimetrico(self):
        print "Efetuando particionamento isoperimetrico de grafo " + self.grafo.obter_nome()
        self.cores_de_vertices = ['g', 'm']
        self.particionamento_de_vertices = self.grafo.obter_particionamento_isoperimetrico()

    def destacar_arestas(self, arestas_a_destacar, cor):
        self.arestas_a_destacar[cor] = arestas_a_destacar

    def obter_grafo_plotado(self):
        plt.axis('off')
        self._desenhar_todos_os_vertices()
        self._desenhar_todas_as_arestas()
        return self.figura

    def _desenhar_todos_os_vertices(self):
        id_cor = -1
        for particao in self.particionamento_de_vertices:
            if id_cor < len(self.cores_de_vertices) - 1:
                id_cor += 1
            self._desenhar_vertices(particao, id_cor)

    def _desenhar_vertices(self, lista_de_vertices, id_cor=-1):
        if id_cor == -1:
            nx.draw_networkx_nodes(self.grafo_nx, self.posicionamento, lista_de_vertices,
                                   node_size=self._obter_tamanho_do_no(),
                                   alpha=0.8)
        else:
            nx.draw_networkx_nodes(self.grafo_nx, self.posicionamento, lista_de_vertices,
                                   node_color=self.cores_de_vertices[id_cor],
                                   node_size=self._obter_tamanho_do_no(),
                                   alpha=0.8)

    def _desenhar_todas_as_arestas(self):
        arestas_do_grafo = self.grafo.obter_lista_de_arestas()
        nx.draw_networkx_edges(self.grafo_nx, self.posicionamento, width=3.0, alpha=1, edgelist=arestas_do_grafo)
        for cor, lista in self.arestas_a_destacar.iteritems():
            nx.draw_networkx_edges(self.grafo_nx,
                                   self.posicionamento,
                                   width=1.0,
                                   alpha=0.5,
                                   edgelist=lista,
                                   edge_color=cor)

    def _obter_tamanho_do_no(self):
        grafo_nx = self.grafo.grafo_nx
        if grafo_nx.order() <= 40:
            return self.tamanhos_dos_nos[0]
        elif grafo_nx.order() <= 60:
            return self.tamanhos_dos_nos[1]
        else:
            return self.tamanhos_dos_nos[2]

    def _adicionar_titulo(self):
        ax = plt.figure().add_subplot(111)
        plt.figure().subplots_adjust(top=0.90)
        ax.set_title("titulo")

    def adicionar_labels(self):
        if self.rotulos == []:
            labels = {}
            for node in self.grafo.grafo_nx.nodes():
                labels[node] = str(int(node) + 1)
        else:
            labels = {}
            i = 0
            for node in self.grafo.grafo_nx.nodes():
                labels[node] = str(self.rotulos[i])
                i += 1

        nx.draw_networkx_labels(self.grafo.grafo_nx,
                                self.posicionamento,
                                labels,
                                font_size=self._obter_tamanho_da_fonte(),
                                ax=None)

    def _obter_tamanho_da_fonte(self):
        grafo_nx = self.grafo.grafo_nx
        if grafo_nx.order() <= 40:
            return self.tamanhos_de_fonte[0]
        elif grafo_nx.order() <= 60:
            return self.tamanhos_de_fonte[1]
        else:
            return self.tamanhos_de_fonte[2]