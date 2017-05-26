import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class DesenhistaDeGrafos:
    def obter_grafo_plotado_de_acordo_com_vetor_fiedler(self, grafo, arestas_sugeridas = None):
        grafo_base = grafo.copia()
        if arestas_sugeridas == None: arestas_sugeridas = []
        for aresta in arestas_sugeridas:
            grafo_base.remover_aresta(aresta)
        verticesPositivos, verticesNegativos = grafo_base.obter_particionamento_pelo_vetor_fiedler()
        return self.obter_grafo_plotado(grafo, [verticesPositivos, verticesNegativos], arestas_sugeridas)

    def obter_grafo_plotado_de_acordo_com_numero_isoperimetrico(self, grafo, arestas_sugeridas = None):
        grafo_base = grafo.copia()
        if arestas_sugeridas == None: arestas_sugeridas = []
        for aresta in arestas_sugeridas:
            if grafo_base.tem_aresta(aresta):
                grafo_base.remover_aresta(aresta)
        vertices_a, vertices_b = grafo_base.obter_particionamento_isoperimetrico()
        return self.obter_grafo_plotado(grafo, [vertices_a, vertices_b], arestas_sugeridas, cores = ['r', 'b'])

    def obter_grafo_plotado(self, grafo, listas_de_vertices, arestas_a_ressaltar, cores):
        grafo_nx = grafo.grafo_nx
        figura = plt.figure()
        plt.axis('off')
        tamanho_do_no = self.obter_tamanho_do_no(grafo)
        tamanho_da_fonte = self.obter_tamanho_da_fonte(grafo)

        pos = nx.circular_layout(grafo_nx, scale=0.5)

        nx.draw_networkx_nodes(grafo_nx, pos, listas_de_vertices[0],
                               node_color='r',
                               node_size=tamanho_do_no,
                               alpha=0.8)
        nx.draw_networkx_nodes(grafo_nx, pos, listas_de_vertices[1],
                               node_color='b',
                               node_size=tamanho_do_no,
                               alpha=0.8)

        arestas_do_grafo = grafo.obter_lista_de_arestas()
        arestas_base = []
        for aresta in arestas_do_grafo:
            if aresta not in arestas_a_ressaltar:
                arestas_base.append(aresta)

        nx.draw_networkx_edges(grafo_nx, pos, width=1.0, alpha=0.5, edgelist=arestas_base)
        indice_da_cor = 0
        for aresta in arestas_a_ressaltar:
            nx.draw_networkx_edges(grafo_nx, pos, width=2.0, alpha=0.5, edgelist=[aresta], edge_color=cores[indice_da_cor])
            indice_da_cor += 1
        labels = {}
        for node in grafo_nx.nodes():
            labels[node] = str(int(node) + 1)
        nx.draw_networkx_labels(grafo_nx, pos, labels, font_size=tamanho_da_fonte, ax=None)
        return figura

    def obter_tamanho_do_no(self, grafo):
        grafo_nx = grafo.grafo_nx
        if grafo_nx.order() <= 40:
            return 750 #/ 5
        elif grafo_nx.order() <= 60:
            return 400 #/ 5
        else:
            return 100 #/ 5

    def obter_tamanho_da_fonte(self, grafo):
        grafo_nx = grafo.grafo_nx
        if grafo_nx.order() <= 40:
            return 15 #/ 3
        elif grafo_nx.order() <= 60:
            return 12
        elif grafo_nx.order() <= 100:
            return 8

    def plotarGrafo(self, G):
        pos = nx.spring_layout(G)
        print pos
        nx.draw_networkx_nodes(G, pos,
                               node_color='b',
                               node_size=500,
                               alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        labels = {}
        for node in G.nodes():
            labels[node] = str(node)
        nx.draw_networkx_labels(G, pos, labels, font_size=10)
        plt.show()
        plt.clf()

    def plotarGrafoEmDiretorioDeAcordoComVetorFiedler(self, descritorDoGrafo, diretorio):
        verticesPositivos, verticesNegativos = descritorDoGrafo.obter_particionamento_pelo_vetor_fiedler()
        grafonx = descritorDoGrafo.grafo_nx
        if grafonx.order() <= 40:
            tamanhoDoNo = 750
            tamanhoDaFonte = 15
        elif grafonx.order() <= 60:
            tamanhoDoNo = 400
            tamanhoDaFonte = 12
        elif grafonx.order() <= 100:
            tamanhoDoNo = 100
            tamanhoDaFonte = 8


        pos = nx.circular_layout(grafonx)
        nx.draw_networkx_nodes(grafonx, pos, verticesPositivos,
                               node_color='r',
                               node_size=tamanhoDoNo,
                               alpha=0.8)
        nx.draw_networkx_nodes(grafonx, pos, verticesNegativos,
                               node_color='b',
                               node_size=tamanhoDoNo,
                               alpha=0.8)


        nx.draw_networkx_edges(grafonx, pos, width=1.0, alpha=0.5)
        labels = {}
        for node in grafonx.nodes():
            labels[node] = str(int(node) + 1)
        nx.draw_networkx_labels(grafonx, pos, labels, font_size=tamanhoDaFonte)
        plt.axis('off')
        #plt.savefig(diretorio)
        plt.show()
        plt.clf()

    def plotar_grafo_na_tela(self, g):
        self.plotarGrafoEmDiretorioDeAcordoComVetorFiedler(g, "")


    #refatorar
    def plotarGrafoEmDiretorioDeAcordoComVetorFiedler_ressaltando_arestas(self, descritorDoGrafo, diretorio, arestas_de_maior_conectividade):
        #for i in range(len(arestas_de_maior_conectividade)):
        #    arestas_de_maior_conectividade[i] =(arestas_de_maior_conectividade[i][0] - 1, arestas_de_maior_conectividade[i][1] - 1)

        verticesPositivos, verticesNegativos = descritorDoGrafo.obter_particionamento_pelo_vetor_fiedler()
        grafonx = descritorDoGrafo.grafo_nx
        if grafonx.order() <= 40:
            tamanhoDoNo = 750
            tamanhoDaFonte = 15
        elif grafonx.order() <= 60:
            tamanhoDoNo = 400
            tamanhoDaFonte = 12
        else:
            tamanhoDoNo = 100
            tamanhoDaFonte = 8


        pos = nx.circular_layout(grafonx)
        nx.draw_networkx_nodes(grafonx, pos, verticesPositivos,
                               node_color='r',
                               node_size=tamanhoDoNo,
                               alpha=0.8)
        nx.draw_networkx_nodes(grafonx, pos, verticesNegativos,
                               node_color='b',
                               node_size=tamanhoDoNo,
                               alpha=0.8)


        nx.draw_networkx_edges(grafonx, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_edges(grafonx, pos, width=3.0, alpha=0.5, edgelist=[arestas_de_maior_conectividade[0]], edge_color='r')
        nx.draw_networkx_edges(grafonx, pos, width=3.0, alpha=0.5, edgelist=[arestas_de_maior_conectividade[1]], edge_color='b')
        labels = {}
        for node in grafonx.nodes():
            labels[node] = str(int(node) + 1)
        nx.draw_networkx_labels(grafonx, pos, labels, font_size=tamanhoDaFonte)

        plt.axis('off')
        plt.savefig(diretorio)
        plt.clf()

        # refatorar
        def plotarGrafoEmDiretorioDeAcordoComVetorFiedler_ressaltando_aresta(self, descritorDoGrafo, diretorio,
                                                                             aresta_de_maior_conectividade):
            aresta_de_maior_conectividade = (aresta_de_maior_conectividade[0] - 1, aresta_de_maior_conectividade[1] - 1)
            verticesPositivos, verticesNegativos = descritorDoGrafo.obter_particionamento_pelo_vetor_fiedler()
            grafonx = descritorDoGrafo.grafo_nx
            if grafonx.order() <= 40:
                tamanhoDoNo = 750
                tamanhoDaFonte = 15
            elif grafonx.order() <= 60:
                tamanhoDoNo = 400
                tamanhoDaFonte = 12
            else:
                tamanhoDoNo = 100
                tamanhoDaFonte = 8

            pos = nx.circular_layout(grafonx)
            nx.draw_networkx_nodes(grafonx, pos, verticesPositivos,
                                   node_color='r',
                                   node_size=tamanhoDoNo,
                                   alpha=0.8)
            nx.draw_networkx_nodes(grafonx, pos, verticesNegativos,
                                   node_color='b',
                                   node_size=tamanhoDoNo,
                                   alpha=0.8)

            nx.draw_networkx_edges(grafonx, pos, width=1.0, alpha=0.5)
            nx.draw_networkx_edges(grafonx, pos, width=5.0, alpha=0.5, edgelist=[aresta_de_maior_conectividade],
                                   edge_color='r')
            labels = {}
            for node in grafonx.nodes():
                labels[node] = str(int(node) + 1)
            nx.draw_networkx_labels(grafonx, pos, labels, font_size=tamanhoDaFonte)
            plt.axis('off')
            plt.savefig(diretorio)
            plt.clf()
