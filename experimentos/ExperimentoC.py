from GeradorDeGrafos import GeradorDeGrafos
from DesenhistaDeGrafos import DesenhistaDeGrafos
from Tabela import Tabela
from AlgoritmoHeuristicaDePerturbacao import AlgoritmoHeuristicaDePerturbacao
from AlgoritmoHeuristicaDeExcentricidadeEGrau import AlgoritmoHeuristicaDeExcentricidadeEGrau
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBrutaAlterado
from GeradorDeHeuristica import GeradorDeHeuristica
from ExperimentoHeuristicaMacap import ExperimentoHeuristicaMacap
import time

'''
O experimento C consiste em gerar todas as arvores T para os casos especiais, ou seja,
aquelas utilizadas no Experimento A cuja melhor aresta a ser inserida (a que
proporcionava o maior aumento da conectividade algebrica) nao incidia no vertice de maior grau,
e registrar algumas de suas propriedades.
'''

class ExperimentoC(ExperimentoHeuristicaMacap):
    def __init__(self):
        self.tabela_de_resultados = Tabela(["D",
                                            "N",
                                            "K",
                                            "L",
                                            "Grafo Original",
                                            "Conectividade Algebrica",
                                            "Arestas Forca Bruta",
                                            "Conectividade Aumentada Forca Bruta",
                                            "Lista de Conectividades",
                                            ],
                                           "Experimento C teste")

    def gerar_grafos(self):
        lista_de_grafos = []
        gerador_de_grafos = GeradorDeGrafos()
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 30, 31, "T(1, 30, 31)"))

        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 38, 38, "T(1, 38, 38)"))

        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 56, 56, "T(1, 56, 56)"))

        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 48, 49, "T(1, 48, 49)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 49, 49, "T(1, 49, 49)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 56, 56, "T(1, 56, 56)"))

        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 59, 60, "T(1, 59, 60)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 66, 67, "T(1, 66, 67)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 67, 67, "T(1, 67, 67)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 74, 74, "T(1, 74, 74)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 77, 78, "T(1, 77, 78)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 81, 81, "T(1, 81, 81)"))

        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 84, 85, "T(1, 84, 85)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 85, 85, "T(1, 85, 85)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 91, 92, "T(1, 91, 92)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 92, 92, "T(1, 92, 92)"))
        #lista_de_grafos.append(gerador_de_grafos.gerar_arvore_t(1, 99, 99, "T(1, 99, 99)"))
        return lista_de_grafos

    def _gerar_dicionario_de_resultados_para_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}

        lista_de_melhores_arestas, lista_de_melhores_conectividades = AlgoritmoHeuristicaDeForcaBrutaAlterado().obter_lista_de_melhores_arestas(grafo)


        dicionario_de_resultados["Arestas Forca Bruta"] = lista_de_melhores_arestas
        dicionario_de_resultados["Lista de Conectividades"] = lista_de_melhores_conectividades

        return dicionario_de_resultados

    def _adicionar_linha_de_resultados(self, grafo, dicionario_de_resultados):
        conectividade_fb = grafo.copia().adicionar_aresta(dicionario_de_resultados["Arestas Forca Bruta"][0]).obter_conectividade_algebrica()
        lista_de_melhores_arestas_formatadas = []
        for aresta in dicionario_de_resultados["Arestas Forca Bruta"]:
            lista_de_melhores_arestas_formatadas.append(self.formatar_aresta(aresta))
        linha = [grafo.obter_diametro(),
                 grafo.obter_ordem(),
                 grafo.obter_k(),
                 grafo.obter_l(),
                 grafo.obter_nome(),
                 grafo.obter_conectividade_algebrica(),
                 lista_de_melhores_arestas_formatadas,
                 conectividade_fb,
                 dicionario_de_resultados["Lista de Conectividades"]
                 ]
        self.tabela_de_resultados.adicionar_linha(linha)


    def executar(self):
        lista_de_grafos = self.gerar_grafos()
        for grafo in lista_de_grafos:
            tempo_inicial = time.time()
            print "Analisando grafo ", grafo.obter_nome()
            self.efetuar_experimento_para_grafo(grafo)
            tempo_final = time.time()
            print "Tempo de analise, " + str(tempo_final - tempo_inicial)
        self.persistir_dados()


'''grafo = GeradorDeGrafos().gerar_arvore_t(1, 38, 38)
print grafo.obter_conectividade_algebrica()
print grafo.copia().adicionar_aresta((10, 70)).obter_conectividade_algebrica()
print grafo.copia().adicionar_aresta((10, 56)).obter_conectividade_algebrica()'''

objeto_experimento_c = ExperimentoC()
objeto_experimento_c.executar()


#lista_de_grafos = ExperimentoB().gerar_grafos()

#for grafo in lista_de_grafos:
#    tabela

#DesenhistaDeGrafos().plotar_grafo_na_tela(ExperimentoB().gerar_grafos().adicionar_aresta((10, 70)))


        #lista_de_grafos.append(GeradorDeGrafos().gerar_arvore_t(1, 38, 38))
        #lista_de_grafos.append(GeradorDeGrafos().gerar_arvore_t(1, 38, 38))
        #lista_de_grafos.append(GeradorDeGrafos().gerar_arvore_t(1, 38, 38))

