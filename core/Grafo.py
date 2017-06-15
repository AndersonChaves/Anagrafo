import networkx as nx
from ParticionadorEspectral import ParticionadorEspectral
from Caminho import Caminho
from AnalisadorDeGrafos import AnalisadorDeGrafos

class Grafo:
    def __init__(self, grafo_nx, nome=""):
        self.grafo_nx = grafo_nx
        self.categoria = ""
        self.nome = nome
        self.vetor_fiedler = []
        self.dicionarioDeDados = {}
        self.diametro = -1
        self.__conectividade_algebrica = -1
        self.scipy_laplaciana = None
        self.analisador = AnalisadorDeGrafos(self)

    def obter_nome(self):
        return self.nome

    def obter_ordem(self):
        return self.grafo_nx.order()

    def obter_lista_de_vertices(self):
        return self.grafo_nx.nodes()

    def obter_diametro(self):
        if self.diametro == -1:
            return nx.diameter(self.grafo_nx)
        else:
            return self.diametro

    def copia(self):
        return Grafo(self.grafo_nx.copy(), self.nome)

    def obter_grafo_equivalente_com_aresta_adicionada(self, aresta):
        novo_nome = self.nome + "+" + str(aresta)
        g = self.grafo_nx.copy()
        g.add_edge(*aresta)
        return Grafo(g, novo_nome)

    def obter_grafo_equivalente_com_arestas_adicionadas(self, lista_de_arestas):
        novo_grafo = self
        for aresta in lista_de_arestas:
            novo_grafo = novo_grafo.obter_grafo_equivalente_com_aresta_adicionada(aresta)
        return novo_grafo

    def obter_grafo_equivalente_removendo_aresta(self, aresta):
        novo_nome = self.nome + "-" + str(aresta)
        return Grafo(self.grafo_nx.copy().remove_edge(*aresta), novo_nome)

    def obter_vetor_fiedler(self):
        return self.analisador.obter_vetor_fiedler()

    def obter_conectividade_algebrica(self):
        return self.analisador.obter_conectividade_algebrica()

    def obter_particionamento_pelo_vetor_fiedler(self):
        return self.analisador.obter_particionamento_pelo_vetor_fiedler()

    def obter_particionamento_isoperimetrico(self):
        return self.analisador.obter_particionamento_isoperimetrico()

    def obter_particionamento_espectral_de_aresta(self, id_no1, id_no2):
        particionador_espectral = ParticionadorEspectral(self)
        return particionador_espectral.obter_particionamento_espectral_de_aresta(id_no1, id_no2)

    def zerar_parametros_calculados(self):
        self.diametro = -1
        self.vetor_fiedler = []
        self.__conectividade_algebrica = -1
        self.scipy_laplaciana = None

    def obter_lista_de_arestas(self):
        return self.grafo_nx.edges()

    def obter_grafo_complemento(self):
        return Grafo(nx.complement(self.grafo_nx))

    def grau_de_vertice(self, vertice):
        return self.grafo_nx.degree(vertice)

    def obter_grau_maximo(self):
        graus = sorted(nx.degree(self.grafo_nx).values(), reverse=True)
        dmax = max(graus)
        return dmax

    def menor_caminho(self, vertice_origem, vertice_destino):
        return nx.shortest_path(self.grafo_nx, vertice_origem, vertice_destino)

    def excentricidade(self, vertice):
        return nx.eccentricity(self.grafo_nx, vertice)

    def obter_laplaciana(self):
        return self.obter_laplaciana_scipy().A

    def obter_laplaciana_scipy(self):
        if self.scipy_laplaciana == None:
            self.scipy_laplaciana = nx.laplacian_matrix(self.grafo_nx)
        return self.scipy_laplaciana

    def obter_todos_os_menores_caminhos_a_partir_de_vertice(self, vertice):
        dicionario_de_caminhos = nx.shortest_path(self.grafo_nx, vertice)
        lista_de_caminhos = []
        for element in dicionario_de_caminhos:
            lista_de_caminhos.append(Caminho(dicionario_de_caminhos[element]))
        return lista_de_caminhos

    #funcao exclusiva para arvores
    def obter_aresta_caracteristica(self):
        return self.analisador.obter_aresta_caracteristica()

    # funcao exclusiva para arvores
    def obter_vertices_caracteristicos(self):
        return self.analisador.obter_vertices_caracteristicos()

    def obter_arestas_de_fronteira_de_particionamento_isoperimetrico(self):
        return self.analisador.obter_arestas_de_fronteira_de_particionamento_isoperimetrico()

    def atribuir_analisador(self, analisador):
        self.analisador = analisador

    def tem_aresta(self, aresta):
        return aresta in self.obter_lista_de_arestas()

    def obter_arestas_de_maior_aumento_isoperimetrico(self):
        return self.analisador.obter_arestas_de_maior_aumento_isoperimetrico()

    def obter_numero_isoperimetrico(self):
        return self.analisador.obter_numero_isoperimetrico()