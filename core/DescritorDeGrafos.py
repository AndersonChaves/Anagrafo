from Grafo import Grafo
import numpy
import networkx as nx
from utils import CalculoDeVetores
from Tabela import Tabela

class Descritor_de_grafos:
    grafo = None

    def __init__(self, grafo):
        self.grafo = grafo

    def gerar_memo_de_informacoes_do_grafo(self):
        texto = 'Grafo:'
        texto += str(self.grafo.obter_nome()) + '\n\n'

        texto += 'Laplaciana:\n'
        texto += str(self.grafo.obter_laplaciana()) + '\n\n'

        texto += 'Conectividade algebrica: '
        texto += str(round(self.grafo.obter_conectividade_algebrica(), 6)) + '\n\n'

        autovalores, autovetores = numpy.linalg.eig(self.grafo.obter_laplaciana())

        autovalores_arredondados = []
        for autovalor in autovalores:
            autovalores_arredondados.append(round(autovalor, 6))

        autovalores_arredondados.sort()
        texto += "Autovalores: "
        texto += str(autovalores_arredondados) + '\n\n'

        autovetores = [[round(i, 2) for i in nested] for nested in autovetores]

        texto += "Autovetores:\n"
        for i in range(len(autovetores)):
            texto += str(autovetores[i]) + '\n'

        texto += '\n'#str(autovetores) + '\n\n'

        texto += "Raio: " + str(nx.radius(self.grafo.grafo_nx)) + '\n'
        texto += "Diametro: %d" % nx.diameter(self.grafo.grafo_nx)+ '\n'
        texto += "Excentricidade: " + str(nx.eccentricity(self.grafo.grafo_nx))+ '\n'
        centro = [v + 1 for v in nx.center(self.grafo.grafo_nx)]
        texto += "Centro: " + str(centro)+ '\n'
        texto += "Vetor Fiedler: " + str(self.grafo.obter_vetor_fiedler())
        #periferia = [v + 1 for v in nx.periphery(self.grafo.grafo_nx)]
        #texto += "Periferia: " + str(periferia)+ '\n'
        #texto += "Densidade: " + str(nx.density(self.grafo.grafo_nx)) + '\n\n'
        texto += "Numero Isoperimetrico: " + str(CalculoDeVetores.calcular_numero_isoperimetrico(self.grafo)) + '\n\n'
        #texto += str(CalculoDeVetores.cheeger(self.grafo))

        return texto