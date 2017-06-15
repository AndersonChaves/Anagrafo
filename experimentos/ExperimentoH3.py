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
import os

"""Descrição do Experimento: Este experimento tem como objetivo verificar o aumento
da conectividade algébrica em grafos do tipo 'starlike', de grau maximo dg = 3 e 4, e n <= (6*dg) + 1. 
quando submetidos aos algoritmos de Heurística de Excentricidade e Heurística de perturbação. 
Este experimento irá verificar o aumento proporcionado pela inclusão 
das arestas sugeridas por he, hp e fb (k=3)."""

class ExperimentoH3(Experimento):
    def __init__(self):
        lista_de_parametros = ["D",
                               "Grau máximo",
                               "Grafo Original",
                               "Conectividade Algebrica",
                               "Arestas Efb*",
                               "G + Efb*",
                               "Aresta Ehp1",
                               "G + Ehp1",
                               "Aresta Ehp2",
                               "G + Ehp2",
                               "Aresta Ehp3",
                               "G + Ehp3",
                               "Aresta Ehe1",
                               "G + Ehe1",
                               "Aresta Ehe2",
                               "G + Ehe2",
                               "Aresta Ehe3",
                               "G + Ehe3",
                               "Melhor Heurística"]
        self.tabela_de_resultados = Tabela(lista_de_parametros,
                                           "ExperimentoH3 - Grau Maximo=5-7 k=3 (1206)")

    def gerar_grafos_a_serem_analisados(self):
        lista_de_grafos = []
        for grau_maximo in [5, 6, 7]:
            ordem_maxima = grau_maximo * 3 + 1
            listas_de_grafos_por_grau_maximo = \
                GeradorDeGrafos().gerar_lista_de_starlikes_de_mesma_altura_por_numero_de_ramos_e_n_maximo(
                    grau_maximo, ordem_maxima)
            lista_de_grafos = lista_de_grafos + listas_de_grafos_por_grau_maximo

        return lista_de_grafos

    def obter_dados_de_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        grafo_hp = grafo.copia()
        grafo_he = grafo.copia()
        numero_de_arestas = 3
        grafo_fb = grafo.copia()

        for k in range(1, numero_de_arestas+1):
            dicionario_de_resultados["aresta_hp" + str(k)] = self.executar_heuristica(grafo_hp, AlgoritmoHeuristicaDePerturbacao())
            dicionario_de_resultados["novo_grafo_hp" + str(k)] = grafo_hp.obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_hp" + str(k)]).copia()

            dicionario_de_resultados["aresta_he" + str(k)] = self.executar_heuristica(grafo_he, AlgoritmoHeuristicaDeExcentricidadeEGrau())
            if dicionario_de_resultados["aresta_he" + str(k)] <> (-1, -1):
                dicionario_de_resultados["novo_grafo_he" + str(k)] = grafo_he.obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_he" + str(k)]).copia()

        dicionario_de_resultados["arestas_fb*"] = self.executar_heuristica(grafo.copia(), AlgoritmoHeuristicaDeForcaBrutaParaMaisDeUmaAresta(numero_de_arestas))
        dicionario_de_resultados["novo_grafo_fb*"] = grafo.copia().obter_grafo_equivalente_com_arestas_adicionadas(dicionario_de_resultados["arestas_fb*"])

        return dicionario_de_resultados

    def obter_dado_correspondente_em_dicionario_de_resultados(self, nome_do_campo, dicionario_de_resultados):
        if   nome_do_campo == "D": return dicionario_de_resultados["grafo"].obter_diametro()
        elif nome_do_campo == "Grau máximo": return dicionario_de_resultados["grafo"].obter_grau_maximo()
        elif nome_do_campo == "Grafo Original":           return dicionario_de_resultados["grafo"].obter_nome()
        elif nome_do_campo == "Conectividade Algebrica":  return dicionario_de_resultados["grafo"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehp1":  return (dicionario_de_resultados["aresta_hp1"][0] + 1, dicionario_de_resultados["aresta_hp1"][1] + 1)
        elif nome_do_campo == "G + Ehp1":     return  dicionario_de_resultados["novo_grafo_hp1"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehp2":  return (dicionario_de_resultados["aresta_hp2"][0] + 1, dicionario_de_resultados["aresta_hp2"][1] + 1)
        elif nome_do_campo == "G + Ehp2":     return  dicionario_de_resultados["novo_grafo_hp2"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehp3":  return (dicionario_de_resultados["aresta_hp3"][0] + 1, dicionario_de_resultados["aresta_hp3"][1] + 1)
        elif nome_do_campo == "G + Ehp3":     return  dicionario_de_resultados["novo_grafo_hp3"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehe1":
            if dicionario_de_resultados["aresta_he1"] <> (-1, -1):
                return (dicionario_de_resultados["aresta_he1"][0] + 1, dicionario_de_resultados["aresta_he1"][1] + 1)
            else:
                return "Grafo nao suportado"

        elif nome_do_campo == "G + Ehe1":
            if dicionario_de_resultados["aresta_he1"] <> (-1, -1):
                return dicionario_de_resultados["novo_grafo_he1"].obter_conectividade_algebrica()
            else:
                return "NA"

        elif nome_do_campo == "Aresta Ehe2":
            if dicionario_de_resultados["aresta_he2"] <> (-1, -1):
                return (dicionario_de_resultados["aresta_he2"][0] + 1, dicionario_de_resultados["aresta_he2"][1] + 1)
            else:
                return "Grafo nao suportado"
        elif nome_do_campo == "G + Ehe2":
            if dicionario_de_resultados["aresta_he2"] <> (-1, -1):
                return  dicionario_de_resultados["novo_grafo_he2"].obter_conectividade_algebrica()
            else:
                return "Grafo nao suportado"
        elif nome_do_campo == "Aresta Ehe3":
            if dicionario_de_resultados["aresta_he3"] <> (-1, -1):
                return (dicionario_de_resultados["aresta_he3"][0] + 1, dicionario_de_resultados["aresta_he3"][1] + 1)
            else:
                return "Grafo nao suportado"
        elif nome_do_campo == "G + Ehe3":
            if dicionario_de_resultados["aresta_he3"] <> (-1, -1):
                return  dicionario_de_resultados["novo_grafo_he3"].obter_conectividade_algebrica()
            else:
                return "Grafo nao suportado"

        elif nome_do_campo == "Melhor Heurística":
            if dicionario_de_resultados["aresta_he3"] == (-1, -1):
                return "NA"
            else:
                if dicionario_de_resultados["novo_grafo_hp3"].obter_conectividade_algebrica() > \
                    dicionario_de_resultados["novo_grafo_he3"].obter_conectividade_algebrica():
                    return "HP"
                elif dicionario_de_resultados["novo_grafo_hp3"].obter_conectividade_algebrica() < \
                    dicionario_de_resultados["novo_grafo_he3"].obter_conectividade_algebrica():
                    return "HE"
                else:
                    return "IGUAIS"
        elif nome_do_campo == "Arestas Efb*":
            return utils.formatar_lista_de_arestas_para_exibicao(dicionario_de_resultados["arestas_fb*"])
        elif nome_do_campo == "G + Efb*":
            return dicionario_de_resultados["novo_grafo_fb*"].obter_conectividade_algebrica()
        else: print "Campo não determinado" + nome_do_campo

    def criar_tabela_de_resultados(self, dados_do_experimento):
        for dicionario_de_resultados in dados_do_experimento:
            posicao = 0
            novo_registro = {}
            for campo in self.tabela_de_resultados.obter_campos():
                novo_registro[posicao] = self.obter_dado_correspondente_em_dicionario_de_resultados(campo, dicionario_de_resultados)
                posicao += 1
            self.tabela_de_resultados.adicionar_linha(novo_registro)
        return self.tabela_de_resultados

    def plotar_grafos_em_diretorio(self, dados_do_experimento):
        path = self.diretorio_do_resultado + "\\Grafos"
        if not os.path.exists(path):
            os.makedirs(path)
        for dicionario_de_resultados in dados_do_experimento:
            grafo_fb = dicionario_de_resultados["novo_grafo_fb*"]
            arestas_fb = dicionario_de_resultados["arestas_fb*"]
            DesenhistaDeGrafos().plotar_grafo_em_diretorio_de_acordo_com_vetor_fiedler_ressaltando_arestas(
                grafo_fb, path + '\\' + grafo_fb.obter_nome(), arestas_fb)

ExperimentoH3().executar_experimento()