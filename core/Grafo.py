import networkx as nx
from ParticionadorEspectral import ParticionadorEspectral
from Caminho import Caminho
from utils import CalculoDeVetores

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

    def obter_nome(self):
        return self.nome

    def obter_ordem(self):
        return self.grafo_nx.order()

    def obter_vetor_fiedler(self):
        if self.vetor_fiedler == []:
            self.vetor_fiedler, self.__conectividade_algebrica = CalculoDeVetores.calcularVetorFiedlerNumpy(self.grafo_nx)
        return self.vetor_fiedler

    def obter_conectividade_algebrica(self):
        if self.__conectividade_algebrica == -1:
            self.vetor_fiedler, self.__conectividade_algebrica = CalculoDeVetores.calcularVetorFiedlerNumpy(self.grafo_nx)
            self.__conectividade_algebrica = round(self.__conectividade_algebrica, 12)
        return self.__conectividade_algebrica

    def obter_lista_de_vertices(self):
        return self.grafo_nx.nodes()

    def obter_particionamento_pelo_vetor_fiedler(self):
        vertices_positivos = []
        vertices_negativos = []
        vetor_fiedler = self.obter_vetor_fiedler()
        for i in range(len(vetor_fiedler)):
            if vetor_fiedler[i] >= 0:
                vertices_positivos.append(self.grafo_nx.nodes()[i])
            else:
                vertices_negativos.append(self.grafo_nx.nodes()[i])
        return vertices_positivos, vertices_negativos

    def obter_particionamento_isoperimetrico(self):
        return CalculoDeVetores.calcular_particionamento_isoperimetrico(self)

    def obter_diametro(self):
        if self.diametro == -1:
            return nx.diameter(self.grafo_nx)
        else:
            return self.diametro

    def obter_particionamento_espectral_de_aresta(self, id_no1, id_no2):
        particionador_espectral = ParticionadorEspectral(self)
        return particionador_espectral.obter_particionamento_espectral_de_aresta(id_no1, id_no2)

    def tem_aresta(self, aresta):
        return self.grafo_nx.has_edge(*aresta)

    def obter_grafo_equivalente_com_aresta_adicionada(self, aresta):
        novo_nome = self.nome + "+" + str(aresta)
        return Grafo(self.grafo_nx.copy().add_edge(*aresta), novo_nome)

    def obter_grafo_equivalente_com_arestas_adicionadas(self, lista_de_arestas):
        novo_grafo = self
        for aresta in lista_de_arestas:
            novo_grafo = novo_grafo.obter_grafo_equivalente_com_aresta_adicionada(aresta)
        return novo_grafo

    def remover_aresta(self, aresta):
        self.grafo_nx.remove_edge(*aresta)
        self.zerar_parametros_calculados()
        return self

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

    def copia(self):
        return Grafo(self.grafo_nx.copy(), self.nome)

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

