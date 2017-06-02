import networkx as nx
import matplotlib.pyplot as plt
import os

class DesenhistaDeGrafos:
    tamanhos_de_fonte = [15, 12, 8]

    def obter_grafo_plotado_de_acordo_com_vetor_fiedler(self, grafo, arestas_sugeridas = None):
        grafo_base = grafo.copia()
        if arestas_sugeridas == None: arestas_sugeridas = []
        for aresta in arestas_sugeridas:
            grafo_base.remover_aresta(aresta)
        verticesPositivos, verticesNegativos = grafo_base.obter_particionamento_pelo_vetor_fiedler()
        return self.obter_grafo_plotado(grafo, [verticesPositivos, verticesNegativos], arestas_sugeridas)

    def plotar_grafo_em_diretorio_de_acordo_com_numero_isoperimetrico(self, grafo, diretorio, *parametros):
        arestas_sugeridas = []
        cores = []
        labels = []
        if len(parametros) > 0:
            arestas_sugeridas = parametros[0]
        if len(parametros) > 1:
            cores = parametros[1]
        else:
            cores = ['g', 'm']
        if len(parametros) > 2:
            labels = parametros[2]

        figura = self.obter_grafo_plotado_de_acordo_com_numero_isoperimetrico(grafo,
                                                                              arestas_sugeridas,
                                                                              cores,
                                                                              labels)
        nome_do_arquivo = grafo.obter_nome() + '.png'
        self.plotar_figura_em_diretorio(figura, diretorio, nome_do_arquivo)

    def obter_grafo_plotado_de_acordo_com_numero_isoperimetrico(self, grafo,
                                                                arestas_sugeridas = None,
                                                                cores = (),
                                                                labels = None):


        grafo_base = grafo.copia()
        if arestas_sugeridas == None: arestas_sugeridas = []
        for lista in arestas_sugeridas:
            for aresta in lista:
                if grafo_base.tem_aresta(aresta):
                    grafo_base.remover_aresta(aresta)

        vertices_a, vertices_b = grafo_base.obter_particionamento_isoperimetrico()

        #rotula os vertices conforme os componentes caracteristicos
        vetor_fiedler = grafo_base.obter_vetor_fiedler()
        self.tamanhos_de_fonte = [12, 10, 7]
        labels, i = {}, 0
        for node in grafo.obter_lista_de_vertices():
            labels[node] = round(vetor_fiedler[i], 2)
            i+=1

        return self.obter_grafo_plotado(grafo, [vertices_a, vertices_b], arestas_sugeridas,
                                        cores_das_arestas = ['r', 'b'], cores_dos_vertices = ['g', 'm'], labels=labels)

    def plotar_figura_em_diretorio(self, figura, diretorio, nome_do_arquivo):
        caminho_do_arquivo = diretorio + '\\' + nome_do_arquivo
        plt.savefig(caminho_do_arquivo)
        plt.clf()

    def obter_grafo_plotado(self, grafo, listas_de_vertices, arestas_a_ressaltar,
                            cores_das_arestas = ('r', 'b'), cores_dos_vertices = ('r', 'b'), labels = None):
        grafo_nx = grafo.grafo_nx
        figura = plt.figure()
        figura.suptitle(grafo.obter_nome(), fontsize=14, fontweight='bold')
        ax = figura.add_subplot(111)
        figura.subplots_adjust(top=0.90)
        ax.set_title('Melhor aresta (vermelho) e aresta isoperimetrica (azul)')

        plt.axis('off')
        tamanho_do_no = self.obter_tamanho_do_no(grafo)
        tamanho_da_fonte = self.obter_tamanho_da_fonte(grafo)

        pos = nx.circular_layout(grafo_nx, scale=0.5)

        nx.draw_networkx_nodes(grafo_nx, pos, listas_de_vertices[0],
                               node_color=cores_dos_vertices[0],
                               node_size=tamanho_do_no,
                               alpha=0.8)
        nx.draw_networkx_nodes(grafo_nx, pos, listas_de_vertices[1],
                               node_color=cores_dos_vertices[1],
                               node_size=tamanho_do_no,
                               alpha=0.8)

        arestas_do_grafo = grafo.obter_lista_de_arestas()
        arestas_base = []
        for aresta in arestas_do_grafo:
            if aresta not in arestas_a_ressaltar:
                arestas_base.append(aresta)

        nx.draw_networkx_edges(grafo_nx, pos, width=1.0, alpha=0.5, edgelist=arestas_base)
        indice_da_cor = 0
        for lista_de_arestas in arestas_a_ressaltar:
            nx.draw_networkx_edges(grafo_nx, pos, width=2.0, alpha=0.5, edgelist=lista_de_arestas, edge_color=cores_das_arestas[indice_da_cor])
            indice_da_cor += 1
        if labels == None:
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
            return self.tamanhos_de_fonte[0] #/ 3
        elif grafo_nx.order() <= 60:
            return self.tamanhos_de_fonte[1]
        elif grafo_nx.order() <= 100:
            return self.tamanhos_de_fonte[2]

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

    #refatorar
    def plotar_grafo_em_diretorio_de_acordo_com_vetor_fiedler_ressaltando_arestas(self, grafo, caminho_do_arquivo, arestas_de_maior_conectividade):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.90)
        ax.set_title('Melhor aresta')


        grafo_base = grafo.copia()
        arestas_sugeridas = arestas_de_maior_conectividade
        for aresta in arestas_sugeridas:
            if grafo_base.tem_aresta(aresta):
                grafo_base.remover_aresta(aresta)

        verticesPositivos, verticesNegativos = grafo_base.obter_particionamento_pelo_vetor_fiedler()

        grafonx = grafo.grafo_nx
        if grafonx.order() <= 40:
            tamanhoDoNo = 750
            tamanhoDaFonte = 15
        elif grafonx.order() <= 60:
            tamanhoDoNo = 400
            tamanhoDaFonte = 12
        else:
            tamanhoDoNo = 100
            tamanhoDaFonte = 8


        pos = nx.shell_layout(grafonx)
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
        nx.draw_networkx_edges(grafonx, pos, width=3.0, alpha=0.5, edgelist=[arestas_de_maior_conectividade[1]], edge_color='r')
        labels = {}
        for node in grafonx.nodes():
            labels[node] = str(int(node) + 1)
        nx.draw_networkx_labels(grafonx, pos, labels, font_size=tamanhoDaFonte)

        plt.suptitle(grafo.obter_nome(), fontsize=14, fontweight='bold')

        plt.axis('off')

        plt.savefig(caminho_do_arquivo)
        plt.clf()