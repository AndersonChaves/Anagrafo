from utils import CalculosDeGrafos
from utils import utils
from AlgoritmoHeuristicaIsoperimetrica import AlgoritmoHeuristicaIsoperimetrica

class AnalisadorDeGrafos():
    parametros_isoperimetricos_ja_calculados = False
    particionamento_isoperimetrico = [[], []]
    arestas_de_fronteira_de_particionamento_isoperimetrico = []
    numero_isoperimetrico = -1

    parametros_espectrais_ja_calculados = False
    vetor_fiedler = []
    conectividade_algebrica = -1
    aresta_caracteristica = ()

    def __init__(self, grafo):
        self.grafo = grafo
        self.grafo.atribuir_analisador(self)

    def obter_particionamento_isoperimetrico(self):
        if not self.parametros_isoperimetricos_ja_calculados:
            self.calcular_parametros_isoperimetricos()
        return self.particionamento_isoperimetrico

    def obter_numero_isoperimetrico(self):
        if not self.parametros_isoperimetricos_ja_calculados:
            self.calcular_parametros_isoperimetricos()
        return self.numero_isoperimetrico

    def obter_arestas_de_fronteira_de_particionamento_isoperimetrico(self):
        if not self.parametros_isoperimetricos_ja_calculados:
            self.calcular_parametros_isoperimetricos()
        return self.arestas_de_fronteira_de_particionamento_isoperimetrico

    def calcular_parametros_isoperimetricos(self):
        parametros = CalculosDeGrafos.calcular_parametros_isoperimetricos(self.grafo)
        self.particionamento_isoperimetrico, self.numero_isoperimetrico = parametros
        self.arestas_de_fronteira_de_particionamento_isoperimetrico = []

        p1, p2 = self.particionamento_isoperimetrico
        for aresta in self.grafo.obter_lista_de_arestas():
            if (aresta[0] in p1) and (aresta[1] in p2) or \
                    (aresta[0] in p2) and (aresta[1] in p1):
                self.arestas_de_fronteira_de_particionamento_isoperimetrico.append(aresta)
        self.parametros_isoperimetricos_ja_calculados = True

    def obter_arestas_de_maior_aumento_isoperimetrico(self):
        alg = AlgoritmoHeuristicaIsoperimetrica()
        alg.executar_algoritmo(self.grafo)
        return alg.obter_lista_de_melhores_arestas()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def obter_vetor_fiedler(self):
        if not self.parametros_espectrais_ja_calculados:
            self.calcular_parametros_espectrais()
        return self.vetor_fiedler

    def obter_conectividade_algebrica(self):
        if not self.parametros_espectrais_ja_calculados:
            self.calcular_parametros_espectrais()
        return self.conectividade_algebrica

    def calcular_parametros_espectrais(self):
        self.vetor_fiedler, self.conectividade_algebrica = CalculosDeGrafos.calcular_vetor_fiedler_numpy(self.grafo.grafo_nx)
        self.conectividade_algebrica = round(self.conectividade_algebrica, 12)
        self.parametros_espectrais_ja_calculados = True

    def obter_particionamento_pelo_vetor_fiedler(self):
        vertices_positivos = []
        vertices_negativos = []
        vetor_fiedler = self.obter_vetor_fiedler()
        for i in range(len(vetor_fiedler)):
            if vetor_fiedler[i] >= 0:
                vertices_positivos.append(self.grafo.grafo_nx.nodes()[i])
            else:
                vertices_negativos.append(self.grafo.grafo_nx.nodes()[i])
        return vertices_positivos, vertices_negativos

    def obter_vertices_caracteristicos(self):
        f = self.obter_vetor_fiedler()
        if 0 in f:
            i = 0
            for e in f:
                if utils.zero(f[i]) and not utils.zero(f[i+1]):
                    self.vertices_caracteristicos = [i]
                    return [i]
                i += 1
        else:
            return list(self.obter_aresta_caracteristica())

    def obter_aresta_caracteristica(self):
        self.obter_vetor_fiedler()

        lista_de_arestas = self.grafo.obter_lista_de_arestas()
        for aresta in lista_de_arestas:
            u, v = aresta
            v1 = self.obter_valor_caracteristico_de_vertice(u)
            v2 = self.obter_valor_caracteristico_de_vertice(v)
            if v1 * v2 < 0:
                self.aresta_caracteristica = aresta
                self.vertices_caracteristicos = list(aresta)
                return aresta
        print "Erro - O grafo nao possui aresta caracteristica"
        raise

    def obter_valor_caracteristico_de_vertice(self, vertice):
        lista = self.grafo.obter_lista_de_vertices()
        return self.obter_vetor_fiedler()[lista.index(vertice)]