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
import time
import os

"""Descrição do Experimento: Este experimento tem como objetivo verificar se há alguma relação
entre a aresta característica e as arestas que incidem simultaneamente em X e X^c(conjunto δX).
Os grafos avaliados são brooms de diâmetro 3 e 4, de até n=50 vértices."""

class ExperimentoI(Experimento):
    def __init__(self):
        lista_de_parametros = ["D",
                               "N",
                               "K",
                               "L",
                               "Grafo Original",
                               "Conectividade Algebrica",
                               "Aresta Caracteristica",
                               "Aresta δX"]
        self.tabela_de_resultados = Tabela(lista_de_parametros,
                                           "Experimento Isoperimetrico I - n= 21 a 25 d=4(1206)")

    def gerar_grafos_a_serem_analisados(self):
        ordem_minima = 21
        ordem_maxima = 25
        listas_de_grafos_por_diametro = []
        for diametro in [4]:
            listas_de_grafos_por_ordem = GeradorDeGrafos().gerar_listas_de_double_brooms_por_diametro_variando_ordem_com_k_fixado(
                ordem_minima=ordem_minima, ordem_maxima = ordem_maxima, diametro = diametro, k = 1)
            listas_de_grafos_por_diametro.append(listas_de_grafos_por_ordem)

        lista_de_grafos = []
        for lista_de_grafos_por_diametro in listas_de_grafos_por_diametro:
                lista_de_grafos = lista_de_grafos + lista_de_grafos_por_diametro
        return lista_de_grafos

    def obter_dados_de_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        if len(grafo.obter_vertices_caracteristicos()) == 2:
            dicionario_de_resultados["aresta_caracteristica"] = grafo.obter_aresta_caracteristica()
        else:
            dicionario_de_resultados["aresta_caracteristica"] = ()
        dicionario_de_resultados["arestas_delta_x"] = grafo.obter_arestas_de_fronteira_de_particionamento_isoperimetrico()
        return dicionario_de_resultados

    def obter_dado_correspondente_em_dicionario_de_resultados(self, nome_do_campo, dicionario_de_resultados):
        if   nome_do_campo == "D": return dicionario_de_resultados["grafo"].obter_diametro()
        elif nome_do_campo == "N": return dicionario_de_resultados["grafo"].obter_ordem()
        elif nome_do_campo == "K": return dicionario_de_resultados["grafo"].obter_k()
        elif nome_do_campo == "L": return dicionario_de_resultados["grafo"].obter_l()
        elif nome_do_campo == "Grafo Original":           return dicionario_de_resultados["grafo"].obter_nome()
        elif nome_do_campo == "Conectividade Algebrica":  return dicionario_de_resultados["grafo"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Caracteristica":  return dicionario_de_resultados["aresta_caracteristica"]
        elif nome_do_campo == "Aresta δX":     return  dicionario_de_resultados["arestas_delta_x"]
        else: print "Campo não determinado" + nome_do_campo

    def criar_tabela_de_resultados(self, dados_do_experimento):
        path = "Resultados\\ExperimentoI\\Grafos"
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
            grafo_a_ser_desenhado = dicionario_de_resultados["grafo"]
            aresta_caracteristica = dicionario_de_resultados["aresta_caracteristica"]
            arestas_delta_x = dicionario_de_resultados["arestas_delta_x"]
            print "Particionando grafo conforme numero isoperimetrico", grafo_a_ser_desenhado.obter_nome()
            tempo_inicial = time.time()
            if aresta_caracteristica != ():
                DesenhistaDeGrafos().plotar_grafo_em_diretorio_de_acordo_com_numero_isoperimetrico(grafo_a_ser_desenhado,
                                                                                                   diretorio,
                                                                                                   [[aresta_caracteristica], arestas_delta_x],
                                                                                                   ['r', 'b']
                                                                                                  )
            else:
                DesenhistaDeGrafos().plotar_grafo_em_diretorio_de_acordo_com_numero_isoperimetrico(grafo_a_ser_desenhado,
                                                                                                   diretorio,
                                                                                                   [arestas_delta_x],
                                                                                                   ['r']
                                                                                                  )

            print "Tempo de particionamento: " + str(time.time() - tempo_inicial) + " segundos"