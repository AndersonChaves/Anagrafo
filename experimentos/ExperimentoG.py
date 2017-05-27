# -*- coding: UTF-8 -*-

from Experimento import Experimento
from core.GeradorDeGrafos import GeradorDeGrafos
from core.DesenhistaDeGrafos import DesenhistaDeGrafos
from core.Tabela import Tabela
from core.utils import utils
from AlgoritmoHeuristicaDePerturbacao import AlgoritmoHeuristicaDePerturbacao
from AlgoritmoHeuristicaDeExcentricidadeEGrau import AlgoritmoHeuristicaDeExcentricidadeEGrau
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBrutaParaMaisDeUmaAresta
from AlgoritmoHeuristicaIsoperimetrica import AlgoritmoHeuristicaIsoperimetrica
import os

"""Descrição do Experimento: Este experimento tem como objetivo verificar se há alguma relação
entre a aresta que maximiza a conectividade algébrica em grafos do tipo 'broom', e o número 
isoperimétrico. Os testes serão realizados em brooms de diâmetro d = 4 a 20, de ordem máxima 20. 
Serão analisadas:
                    a. A aresta que maximiza a conectividade algébrica
                    b. A aresta que maximiza o número isoperímétrico
                    c. Os valores característicos dos vértices"""

class ExperimentoG(Experimento):
    def __init__(self):
        lista_de_parametros = ["D",
                               "N",
                               "K",
                               "L",
                               "Grafo Original",
                               "Conectividade Algebrica",
                               "Aresta Efb",
                               "G + Efb",
                               "Aresta Eis",
                               "G + Eis"]
        self.tabela_de_resultados = Tabela(lista_de_parametros,
                                           "Experimento Isoperimetrico 1 - d=4a10")

    def gerar_grafos_a_serem_analisados(self):
        ordem_maxima = 10
        listas_de_grafos_por_diametro = []
        for diametro in range(4, 5): #41
            listas_de_grafos_por_ordem = GeradorDeGrafos().gerar_listas_de_arvores_t_por_diametro_variando_ordem_com_k_fixado(
                ordem_maxima = ordem_maxima, diametro = diametro, k = 1)
            listas_de_grafos_por_diametro.append(listas_de_grafos_por_ordem)

        lista_de_grafos = []
        for lista_de_grafos_por_diametro in listas_de_grafos_por_diametro:
                lista_de_grafos = lista_de_grafos + lista_de_grafos_por_diametro
        return lista_de_grafos

    def obter_dados_de_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        grafo_fb = grafo.copia()
        grafo_is = grafo.copia()
        dicionario_de_resultados["aresta_fb"] = self.executar_heuristica(grafo_fb, AlgoritmoHeuristicaDeForcaBruta())
        dicionario_de_resultados["novo_grafo_fb"] = grafo_fb.adicionar_aresta(dicionario_de_resultados["aresta_fb"]).copia()
        dicionario_de_resultados["aresta_is"] = self.executar_heuristica(grafo_is, AlgoritmoHeuristicaIsoperimetrica())
        dicionario_de_resultados["novo_grafo_is"] = grafo_is.adicionar_aresta(dicionario_de_resultados["aresta_is"]).copia()
        return dicionario_de_resultados

    def obter_dado_correspondente_em_dicionario_de_resultados(self, nome_do_campo, dicionario_de_resultados):
        if   nome_do_campo == "D": return dicionario_de_resultados["grafo"].obter_diametro()
        elif nome_do_campo == "N": return dicionario_de_resultados["grafo"].obter_ordem()
        elif nome_do_campo == "K": return dicionario_de_resultados["grafo"].obter_k()
        elif nome_do_campo == "L": return dicionario_de_resultados["grafo"].obter_l()
        elif nome_do_campo == "Grafo Original":           return dicionario_de_resultados["grafo"].obter_nome()
        elif nome_do_campo == "Conectividade Algebrica":  return dicionario_de_resultados["grafo"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Efb":  return (dicionario_de_resultados["aresta_fb"][0] + 1, dicionario_de_resultados["aresta_fb"][1] + 1)
        elif nome_do_campo == "G + Efb":     return  dicionario_de_resultados["novo_grafo_fb"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Eis":  return (dicionario_de_resultados["aresta_is"][0] + 1, dicionario_de_resultados["aresta_is"][1] + 1)
        elif nome_do_campo == "G + Eis":     return  dicionario_de_resultados["novo_grafo_is"].obter_conectividade_algebrica()
        else: print "Campo não determinado" + nome_do_campo

    def criar_tabela_de_resultados(self, dados_do_experimento):
        path = "Resultados\\ExperimentoF\\Grafos"
        for dicionario_de_resultados in dados_do_experimento:
            posicao = 0
            novo_registro = {}
            for campo in self.tabela_de_resultados.obter_campos():
                novo_registro[posicao] = self.obter_dado_correspondente_em_dicionario_de_resultados(campo, dicionario_de_resultados)
                posicao += 1
            self.tabela_de_resultados.adicionar_linha(novo_registro)
        return self.tabela_de_resultados

    def plotar_grafos_em_diretorio(self, dados_do_experimento):
        diretorio = self.diretorio_do_resultado + '\\Grafos'
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        for dicionario_de_resultados in dados_do_experimento:
            grafo_a_ser_desenhado = dicionario_de_resultados["novo_grafo_fb"]
            aresta_fb = dicionario_de_resultados["aresta_fb"]
            aresta_is = dicionario_de_resultados["aresta_is"]
            DesenhistaDeGrafos().plotar_grafo_em_diretorio_de_acordo_com_numero_isoperimetrico(grafo_a_ser_desenhado,
                                                                                               diretorio,
                                                                                               [aresta_fb, aresta_is],
                                                                                              )