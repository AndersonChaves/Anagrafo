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

"""Experimento de testes, para corrigir problemas no experimento E anterior"""

class ExperimentoTeste(Experimento):
    def __init__(self):
        lista_de_parametros = ["D",
                               "N",
                               "K",
                               "L",
                               "Grafo Original",
                               "Conectividade Algebrica",
                               #"Aresta Efb1",
                               #"G + Efb1",
                               #"Aresta Efb2",
                               #"G + Efb2",
                               "Arestas Efb*",
                               "G + Efb*"
                               #"Aresta Ehp1",
                               #"G + Ehp1",
                               #"Aresta Ehp2",
                               #"G + Ehp2",
                               #"Aresta Ehe1",
                               #"G + Ehe1",
                               #"Aresta Ehe2",
                               #"G + Ehe2",
                               ]#"Melhor Heurística"]
        self.tabela_de_resultados = Tabela(lista_de_parametros,
                                           "ExperimentoE - d=3 (2905)")

    #def gerar_grafos_a_serem_analisados(self):
    #    ordem_maxima = 20
    #    listas_de_grafos_por_diametro = []
    #    for diametro in range(9, 16):
    #        listas_de_grafos_por_ordem = GeradorDeGrafos().gerar_listas_de_double_brooms_por_diametro_variando_ordem_com_k_fixado(
    #            ordem_maxima = ordem_maxima, diametro = diametro, k = 1)
    #        listas_de_grafos_por_diametro.append(listas_de_grafos_por_ordem)

    #    lista_de_grafos = []
    #    for lista_de_grafos_por_diametro in listas_de_grafos_por_diametro:
    #            lista_de_grafos = lista_de_grafos + lista_de_grafos_por_diametro
    #    return lista_de_grafos

    def gerar_grafos_a_serem_analisados(self):
        ordem_maxima = 20
        listas_de_grafos_por_diametro = []
        for diametro in [3, 4]:
            listas_de_grafos_por_ordem = GeradorDeGrafos().gerar_listas_de_double_brooms_por_diametro_variando_ordem(ordem_maxima, diametro)
            listas_de_grafos_por_diametro.append(listas_de_grafos_por_ordem)

        lista_de_grafos = []
        for listas_de_grafos_por_ordem in listas_de_grafos_por_diametro:
            for lista in listas_de_grafos_por_ordem:
                lista_de_grafos = lista_de_grafos + lista
        return lista_de_grafos

    def obter_dados_de_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        grafo_hp = grafo.copia()
        grafo_he = grafo.copia()
        grafo_fb = grafo.copia()
        #for k in range(1, 3):
            #dicionario_de_resultados["aresta_hp" + str(k)] = self.executar_heuristica(grafo_hp, AlgoritmoHeuristicaDePerturbacao())
            #dicionario_de_resultados["novo_grafo_hp" + str(k)] = grafo_hp.obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_hp" + str(k)]).copia()

            #dicionario_de_resultados["aresta_he" + str(k)] = self.executar_heuristica(grafo_he, AlgoritmoHeuristicaDeExcentricidadeEGrau())
            #dicionario_de_resultados["novo_grafo_he" + str(k)] = grafo_he.obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_he" + str(k)]).copia()

            #dicionario_de_resultados["aresta_fb" + str(k)] = self.executar_heuristica(grafo_fb, AlgoritmoHeuristicaDeForcaBruta())
            #dicionario_de_resultados["novo_grafo_fb" + str(k)] = grafo_fb.obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb" + str(k)]).copia()

        dicionario_de_resultados["arestas_fb*"] = self.executar_heuristica(grafo.copia(),
                                                                           AlgoritmoHeuristicaDeForcaBrutaParaMaisDeUmaAresta())
        dicionario_de_resultados["novo_grafo_fb*"] = grafo.copia().obter_grafo_equivalente_com_arestas_adicionadas(
            dicionario_de_resultados["arestas_fb*"])
        return dicionario_de_resultados

    def obter_dado_correspondente_em_dicionario_de_resultados(self, nome_do_campo, dicionario_de_resultados):
        if   nome_do_campo == "D": return dicionario_de_resultados["grafo"].obter_diametro()
        elif nome_do_campo == "N": return dicionario_de_resultados["grafo"].obter_ordem()
        elif nome_do_campo == "K": return dicionario_de_resultados["grafo"].obter_k()
        elif nome_do_campo == "L": return dicionario_de_resultados["grafo"].obter_l()
        elif nome_do_campo == "Grafo Original":           return dicionario_de_resultados["grafo"].obter_nome()
        elif nome_do_campo == "Conectividade Algebrica":  return dicionario_de_resultados["grafo"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Efb1":  return (dicionario_de_resultados["aresta_fb1"][0] + 1, dicionario_de_resultados["aresta_fb1"][1] + 1)
        elif nome_do_campo == "G + Efb1":     return  dicionario_de_resultados["novo_grafo_fb1"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Efb2":  return (dicionario_de_resultados["aresta_fb2"][0] + 1, dicionario_de_resultados["aresta_fb2"][1] + 1)
        elif nome_do_campo == "G + Efb2":     return  dicionario_de_resultados["novo_grafo_fb2"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehp1":  return (dicionario_de_resultados["aresta_hp1"][0] + 1, dicionario_de_resultados["aresta_hp1"][1] + 1)
        elif nome_do_campo == "G + Ehp1":     return  dicionario_de_resultados["novo_grafo_hp1"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehp2":  return (dicionario_de_resultados["aresta_hp2"][0] + 1, dicionario_de_resultados["aresta_hp2"][1] + 1)
        elif nome_do_campo == "G + Ehp2":     return  dicionario_de_resultados["novo_grafo_hp2"].obter_conectividade_algebrica()
        elif nome_do_campo == "Aresta Ehe1":  return (dicionario_de_resultados["aresta_he1"][0] + 1, dicionario_de_resultados["aresta_he1"][1] + 1)
        elif nome_do_campo == "G + Ehe1":     return  dicionario_de_resultados["novo_grafo_he1"].obter_conectividade_algebrica()

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

        elif nome_do_campo == "Melhor Heurística":
            if dicionario_de_resultados["aresta_he2"] == (-1, -1):
                return "NA"
            else:
                if dicionario_de_resultados["novo_grafo_hp2"].obter_conectividade_algebrica() > \
                    dicionario_de_resultados["novo_grafo_he2"].obter_conectividade_algebrica():
                    return "HP"
                elif dicionario_de_resultados["novo_grafo_hp2"].obter_conectividade_algebrica() < \
                    dicionario_de_resultados["novo_grafo_he2"].obter_conectividade_algebrica():
                    return "HE"
                else:
                    return "IGUAIS"
        elif nome_do_campo == "Arestas Efb*":
            return utils.formatar_lista_de_arestas_para_exibicao(dicionario_de_resultados["arestas_fb*"])
        elif nome_do_campo == "G + Efb*":
            return dicionario_de_resultados["novo_grafo_fb*"].obter_conectividade_algebrica()
        else: print "Campo não determinado" + nome_do_campo

    def criar_tabela_de_resultados(self, dados_do_experimento):
        path = "Resultados\\ExperimentoF\\Grafos"
        for dicionario_de_resultados in dados_do_experimento:
            grafo_fb = dicionario_de_resultados["novo_grafo_fb*"]
            arestas_fb = dicionario_de_resultados["arestas_fb*"]
            #grafo_hp = dicionario_de_resultados["novo_grafo_hp2"]
            #arestas_hp = [dicionario_de_resultados["aresta_hp1"], dicionario_de_resultados["aresta_hp2"]]
            #grafo_he = dicionario_de_resultados["novo_grafo_he2"]
            #arestas_he = [dicionario_de_resultados["aresta_he1"], dicionario_de_resultados["aresta_he2"]]
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
            grafo_fb = dicionario_de_resultados["novo_grafo_fb*"]
            arestas_fb = dicionario_de_resultados["arestas_fb*"]
            DesenhistaDeGrafos().plotar_grafo_em_diretorio_de_acordo_com_vetor_fiedler_ressaltando_arestas(
                grafo_fb, diretorio + '\\' + grafo_fb.obter_nome(), arestas_fb)

