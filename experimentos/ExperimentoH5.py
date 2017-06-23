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
da conectividade algébrica em grafos do tipo 'starlike', de diversos graus máximos (dg) e de diversos diâmetros,
quando submetidos aos algoritmos de Heurística de Excentricidade e Heurística de perturbação. 
Este experimento irá verificar o aumento proporcionado pela inclusão 
das arestas sugeridas por he, hp e fb. O número de arestas será sempre k=dg-2 e k=dg-1."""

class ExperimentoH4(Experimento):
    numero_de_arestas = 3
    tamanho_do_caminho = 2
    grau_maximo = 3
    grau_minimo = 1
    recriar_tabela = False

    def __init__(self):
        self.obter_lista_de_campos_da_tabela_de_resultados()
        lista_de_parametros = self.obter_lista_de_campos_da_tabela_de_resultados()
        self.tabela_de_resultados = Tabela(lista_de_parametros,
                                           "Experimento H4 - k=4 dg=5, caminho=2")

    def obter_lista_de_campos_da_tabela_de_resultados(self):
        lista_de_parametros = ["D",
                                "Grau máximo",
                                "Grafo Original",
                                "Conectividade Algebrica",
                                "Arestas Efb*",
                                "G + Efb*"]
        for i in range(1, self.numero_de_arestas + 1):
            lista_de_parametros.append("Aresta Ehp" + str(i))
            lista_de_parametros.append("G + Ehp" + str(i))
            lista_de_parametros.append("Aresta Ehe" + str(i))
            lista_de_parametros.append("G + Ehe" + str(i))
        lista_de_parametros.append("Melhor Heurística")
        return lista_de_parametros

    def gerar_grafos_a_serem_analisados(self):
        lista_de_grafos = []
        for grau_maximo in [5]:
            ordem_maxima = grau_maximo * 3 + 1
            lista_de_graus = self.gerar_lista_de_graus()
            listas_de_grafos_por_grau_maximo = [GeradorDeGrafos().gerar_starlike(lista_de_graus)]
            lista_de_grafos = lista_de_grafos + listas_de_grafos_por_grau_maximo

        return lista_de_grafos

    def gerar_lista_de_graus(self):
        lista = []
        for i in range(self.grau_maximo+1):
            lista.append(self.tamanho_do_caminho)
        return lista

    def obter_dados_de_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        grafo_hp = grafo.copia()
        grafo_he = grafo.copia()
        numero_de_arestas = self.numero_de_arestas
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

    def formatar_registro_de_tabela_de_resultados(self, dicionario_de_resultados):
        novo_registro = {}
        novo_registro["D"] = dicionario_de_resultados["grafo"].obter_diametro()
        novo_registro["Grau máximo"] = dicionario_de_resultados["grafo"].obter_grau_maximo()
        novo_registro["Grafo Original"] = dicionario_de_resultados["grafo"].obter_nome()
        novo_registro["Conectividade Algebrica"] = dicionario_de_resultados["grafo"].obter_conectividade_algebrica()
        for i in range(1, self.numero_de_arestas+1):
            aresta_hp = dicionario_de_resultados["aresta_hp" + str(i)]
            campo_aresta = "Aresta Ehp" + str(i)
            campo_conectividade = "G + Ehp" + str(i)
            novo_registro[campo_aresta] = (aresta_hp[0]+1, aresta_hp[1]+1)
            novo_registro[campo_conectividade] = dicionario_de_resultados["novo_grafo_hp" + str(i)].obter_conectividade_algebrica()

            aresta_he = dicionario_de_resultados["aresta_he" + str(i)]
            if aresta_he != (-1, -1):
                campo_aresta = "Aresta Ehe" + str(i)
                campo_conectividade = "G + Ehe" + str(i)

                novo_registro[campo_aresta] = (aresta_he[0]+1, aresta_he[1]+1)
                novo_registro[campo_conectividade] = dicionario_de_resultados["novo_grafo_he" + str(i)].obter_conectividade_algebrica()
            else:
                campo_aresta = "Aresta Ehe" + str(i)
                campo_conectividade = "G + Ehe" + str(i)
                novo_registro[campo_aresta] = "Grafo nao suportado"
                novo_registro[campo_conectividade] = "NA"
        conectividade_hp = novo_registro["G + Ehp1"]
        conectividade_he = novo_registro["G + Ehe1"]
        if conectividade_he == "NA":
            novo_registro["Melhor Heurística"] = "NA"
        elif conectividade_hp > conectividade_he:
            novo_registro["Melhor Heurística"] = "HP"
        elif conectividade_he > conectividade_hp:
            novo_registro["Melhor Heurística"] = "HE"
        else:
            novo_registro["Melhor Heurística"] = "IGUAIS"

        novo_registro["Arestas Efb*"] = utils.formatar_lista_de_arestas_para_exibicao(dicionario_de_resultados["arestas_fb*"])
        novo_registro["G + Efb*"] = dicionario_de_resultados["novo_grafo_fb*"].obter_conectividade_algebrica()
        return novo_registro


    def criar_tabela_de_resultados(self, dados_do_experimento):
        for dicionario_de_resultados in dados_do_experimento:
            novo_registro = {}
            posicao = 0

            dicionario_de_resultados_formatado = self.formatar_registro_de_tabela_de_resultados(dicionario_de_resultados)
            for campo in self.tabela_de_resultados.obter_campos():
                novo_registro[posicao] = dicionario_de_resultados_formatado[campo]
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

ExperimentoH4().executar_experimento()