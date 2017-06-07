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

class ExperimentoB(ExperimentoHeuristicaMacap):
    def __init__(self):
        self.tabela_de_resultados = Tabela(["D",
                                            "N",
                                            "K",
                                            "L",
                                            "Grafo Original",
                                            "Conectividade Algebrica",
                                            "Aresta HP",
                                            "Conectividade Aumentada HP",
                                            "Aresta HE",
                                            "Conectividade Aumentada HE",
                                            "Aresta FB1",
                                            "Conectividade Aumentada FB",
                                            "Aresta FB2",
                                            "Conectividade Aumentada FB2",
                                            "Melhor Heuristica"],
                                           "Experimento B.2")

    def gerar_grafos(self):
        lista_de_grafos = []
        gerador_de_grafos = GeradorDeGrafos()
        #lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 30, 31, "T(1, 30, 31)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 38, 38, "T(1, 38, 38)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 56, 56, "T(1, 56, 56)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 48, 49, "T(1, 48, 49)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 49, 49, "T(1, 49, 49)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 56, 56, "T(1, 56, 56)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 59, 60, "T(1, 59, 60)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 66, 67, "T(1, 66, 66)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 67, 67, "T(1, 67, 67)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 74, 74, "T(1, 74, 74)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 77, 78, "T(1, 77, 78)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 81, 81, "T(1, 81, 81)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 84, 85, "T(1, 84, 85)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 85, 85, "T(1, 85, 85)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 91, 92, "T(1, 91, 92)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 92, 92, "T(1, 92, 92)"))
        lista_de_grafos.append(gerador_de_grafos.gerar_double_broom(1, 99, 99, "T(1, 99, 99)"))
        return lista_de_grafos

    def _gerar_dicionario_de_resultados_para_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        dicionario_de_resultados["aresta_hp"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDePerturbacao())
        dicionario_de_resultados["novo_grafo_hp"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_hp"])

        dicionario_de_resultados["aresta_he"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDeExcentricidadeEGrau())
        dicionario_de_resultados["novo_grafo_he"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_he"])

        dicionario_de_resultados["aresta_fb"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDeForcaBruta())
        dicionario_de_resultados["novo_grafo_fb"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb"])

        dicionario_de_resultados["aresta_fb2"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDeForcaBrutaAlterado())
        dicionario_de_resultados["novo_grafo_fb2"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb2"])
        print dicionario_de_resultados["aresta_fb2"]

        return dicionario_de_resultados

    def _adicionar_linha_de_resultados(self, grafo, dicionario_de_resultados):
        conectividade_hp = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_hp"]).obter_conectividade_algebrica()
        conectividade_he = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_he"]).obter_conectividade_algebrica()
        conectividade_fb = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb"]).obter_conectividade_algebrica()
        conectividade_fb2 = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb2"]).obter_conectividade_algebrica()

        linha = [grafo.obter_diametro(),
                 grafo.obter_ordem(),
                 grafo.obter_k(),
                 grafo.obter_l(),
                 grafo.obter_nome(),
                 grafo.obter_conectividade_algebrica(),
                 self.formatar_aresta(dicionario_de_resultados["aresta_hp"]),
                 conectividade_hp,
                 self.formatar_aresta(dicionario_de_resultados["aresta_he"]),
                 conectividade_he,
                 self.formatar_aresta(dicionario_de_resultados["aresta_fb"]),
                 conectividade_fb,
                 self.formatar_aresta(dicionario_de_resultados["aresta_fb2"]),
                 conectividade_fb2
                 ]
        if conectividade_hp > conectividade_he:
            linha.append("HP")
        elif conectividade_he > conectividade_hp:
            linha.append("HE")
        else:
            linha.append("Iguais")

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

#objeto_experimento_b = ExperimentoB()
#objeto_experimento_b.executar()

'''grafo = GeradorDeGrafos().gerar_double_broom(1, 38, 38, "T(1, 38, 38)")
print grafo.obter_conectividade_algebrica()
print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((10, 70)).obter_conectividade_algebrica()
print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((0, 37)).obter_conectividade_algebrica()


DesenhistaDeGrafos().plotar_grafo_na_tela(grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((0, 37)))
DesenhistaDeGrafos().plotar_grafo_na_tela(grafo)

grafo = GeradorDeGrafos().gerar_double_broom(1, 56, 56, "T(1, 56, 56)")
print grafo.obter_conectividade_algebrica()
print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((15, 109)).obter_conectividade_algebrica()
print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((15, 55)).obter_conectividade_algebrica()
'''
#grafo = GeradorDeGrafos().gerar_double_broom(1, 56, 56, "T(1, 56, 56)")
#print grafo.obter_conectividade_algebrica()
#print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((15, 110)).obter_conectividade_algebrica()

grafo = GeradorDeGrafos().gerar_double_broom(1, 56, 56, "T(1, 56, 56)")


#print grafo.obter_grafo_equivalente_com_aresta_adicionada((10, 37)).obter_conectividade_algebrica()
'''print "Melhores Arestas"
lista = [(14, 55), (15, 55), (15, 56), (15, 57), (15, 58), (15, 59), (15, 60), (15, 61), (15, 62), (15, 63), (15, 64),
         (15, 65), (15, 66), (15, 67), (15, 68), (15, 69), (15, 70), (15, 71), (15, 72), (15, 73), (15, 74), (15, 75),
         (15, 76), (15, 77), (15, 78), (15, 79), (15, 80), (15, 81), (15, 82), (15, 83), (15, 84), (15, 85), (15, 86),
         (15, 87), (15, 88), (15, 89), (15, 90), (15, 91), (15, 92), (15, 93), (15, 94), (15, 95), (15, 96), (15, 97),
         (15, 98), (15, 99), (15, 100), (15, 101), (15, 102), (15, 103), (15, 104), (15, 105), (15, 106), (15, 107),
         (15, 108), (15, 109), (15, 110), (15, 111), (16, 54), (16, 55)]

for aresta in lista:
    print aresta, grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(aresta).obter_conectividade_algebrica()
'''




print grafo.obter_conectividade_algebrica()
print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((15, 55)).obter_conectividade_algebrica()
print grafo.copia().obter_grafo_equivalente_com_aresta_adicionada((15, 56)).obter_conectividade_algebrica()




#lista_de_grafos = ExperimentoB().gerar_grafos()

#for grafo in lista_de_grafos:
#    tabela

#DesenhistaDeGrafos().plotar_grafo_na_tela(ExperimentoB().gerar_grafos().obter_grafo_equivalente_com_aresta_adicionada((10, 70)))

#print ExperimentoB().gerar_grafos().obter_grafo_equivalente_com_aresta_adicionada((10, 70)).obter_conectividade_algebrica()
#print ExperimentoB().gerar_grafos().obter_grafo_equivalente_com_aresta_adicionada((10, 37)).obter_conectividade_algebrica()


        #lista_de_grafos = []
        #lista_de_grafos.append(GeradorDeGrafos().gerar_double_broom(1, 38, 38))
        #lista_de_grafos.append(GeradorDeGrafos().gerar_double_broom(1, 38, 38))
        #lista_de_grafos.append(GeradorDeGrafos().gerar_double_broom(1, 38, 38))
