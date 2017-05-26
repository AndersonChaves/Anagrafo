from AlgoritmoDeHeuristicaDeConectividadeAlgebrica import AlgoritmoDeHeuristicaDeConectividadeAlgebrica

class AlgoritmoHeuristicaDeExcentricidadeEGrau(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_candidatas = self.obter_arestas_candidatas(grafo)
        if len(arestas_candidatas) == 0:
            #raise ErroDeGrafoNaoSuportado
            return (-1, -1)
        aresta_escolhida = self.selecionar_aresta_mais_adequada_dentre_candidatas(arestas_candidatas, grafo)
        return aresta_escolhida

    def obter_arestas_candidatas(self, grafo):
        diametro = grafo.obter_diametro()
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()

        arestas_candidatas = self.filtrar_arestas_por_distancia_de_extremidades(arestas_complementares, grafo, diametro - 1)
        #print "Arestas Candidatas com distancia correta", arestas_candidatas

        arestas_candidatas = self.filtrar_arestas_por_valor_de_excentricidade_das_extremidades(arestas_candidatas, grafo, diametro, diametro - 1)
        #print "Arestas Candidatas com excentricidade correta", arestas_candidatas

        return arestas_candidatas

    def selecionar_aresta_mais_adequada_dentre_candidatas(self, lista_de_arestas, grafo):
        # Filtrar as arestas cujo vertice de maior excentricidade possui grau maximo.
        lista_filtrada = []
        maior_grau = -1
        for aresta in lista_de_arestas:
            a, b = self.ordenar_vertices_por_valor_de_excentricidade(aresta, grafo)
            if grafo.grau_de_vertice(a) > maior_grau:
                lista_filtrada = [aresta]
                maior_grau = grafo.grau_de_vertice(a)
            elif grafo.grau_de_vertice(a) == maior_grau:
                lista_filtrada.append(aresta)

        #print "Arestas Candidatas com vertice de maior grau", lista_filtrada

        #Filtrar arestas cujo vertice de menor excentricidade possua grau maximo
        if len(lista_filtrada) > 1:
            lista_de_arestas = lista_filtrada
            lista_filtrada = []
            maior_grau = -1
            for aresta in lista_de_arestas:
                a, b = self.ordenar_vertices_por_valor_de_excentricidade(aresta, grafo)
                if grafo.grau_de_vertice(b) > maior_grau:
                    lista_filtrada = [aresta]
                    maior_grau = grafo.grau_de_vertice(b)
                elif grafo.grau_de_vertice(b) == maior_grau:
                    lista_filtrada.append(aresta)

        return lista_filtrada[0]

    def filtrar_por_arestas_cujas_extremidades_nao_sao_folhas(self, grafo, lista_de_arestas):
        lista_filtrada = []
        for aresta in lista_de_arestas:
            a, b = aresta
            if grafo.grau_de_vertice(a) > 1 or grafo.grau_de_vertice(b) > 1:
                lista_filtrada.append((a, b))
        return lista_filtrada

    def filtrar_arestas_por_distancia_de_extremidades(self, lista_de_arestas, grafo, distancia_desejada):
        lista_filtrada = []
        for aresta in lista_de_arestas:
            distancia = len(grafo.menor_caminho(*aresta)) - 1
            if distancia == distancia_desejada:
                lista_filtrada.append(aresta)
        return lista_filtrada

    def filtrar_arestas_por_valor_de_excentricidade_das_extremidades(self, lista_de_arestas, grafo,  excentricidade_desejada_1,
                                                                     excentricidade_desejada_2):
        lista_filtrada = []
        for aresta in lista_de_arestas:
            ex1, ex2 = grafo.excentricidade(aresta[0]), grafo.excentricidade(aresta[1])
            if (ex1 == excentricidade_desejada_1 and ex2 == excentricidade_desejada_2) or \
               (ex2 == excentricidade_desejada_1 and ex1 == excentricidade_desejada_2):
                lista_filtrada.append(aresta)
        return lista_filtrada

    def ordenar_vertices_por_valor_de_excentricidade(self, aresta, grafo):
        if grafo.excentricidade(aresta[0]) < grafo.excentricidade(aresta[1]):
            aresta = (aresta[1], aresta[0])
        return aresta

    def identificar_vertice_de_maior_excentricidade_em_aresta(self, aresta, grafo):
        if grafo.excentricidade(aresta[0]) >= grafo.excentricidade(aresta[1]):
            return aresta[0]
        else:
            return aresta[1]

    def identificar_grau_de_excentricidade(self, vertice, grafo):
        excentricidade = grafo.excentricidade(vertice)
        menores_caminhos = grafo.obter_todos_os_menores_caminhos_a_partir_de_vertice(vertice)
        grau_de_excentricidade = 0
        for caminho in menores_caminhos:
            if caminho.tamanho == excentricidade:
                grau_de_excentricidade += 1
        return grau_de_excentricidade

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Excentricidade e Grau"


class ErroDeGrafoNaoSuportado(Exception):
   """Erro de Grafo Nao suportado"""
   pass

'''import networkx as nx
from Grafo import Grafo
g = nx.Graph()
g.add_nodes_from(range(1, 8))

g.add_edges_from([(1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 8), (6, 7), (7, 8)])

grafo = Grafo(g)

alg = AlgoritmoHeuristicaDeExcentricidadeEGrau()

a = alg.executar_algoritmo(grafo)

print a'''

