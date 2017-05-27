# -*- coding: UTF-8 -*-

import core
from core.GeradorDeGrafos import GeradorDeGrafos
from core.DesenhistaDeGrafos import DesenhistaDeGrafos
from core.Tabela import Tabela
from AlgoritmoHeuristicaDePerturbacao import AlgoritmoHeuristicaDePerturbacao
from AlgoritmoHeuristicaDeExcentricidadeEGrau import AlgoritmoHeuristicaDeExcentricidadeEGrau
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from abc import ABCMeta, abstractmethod
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBrutaAlterado
from GeradorDeHeuristica import GeradorDeHeuristica
from ExperimentoHeuristicaMacap import ExperimentoHeuristicaMacap
from core.DescritorDeGrafos import Descritor_de_grafos
from core.EscritorDeDados import EscritorDeDados
import time

"""Esta é a classe base para todos os experimentos que forem ser realizados. """

class Experimento():
    __metaclass__ = ABCMeta #Classe abstrata
    diretorio_do_resultado = "Resultados"
    tabela_de_resultados = None


    def executar_experimento(self):
        tempo_inicial = time.time()
        print "Iniciando Experimento"

        grafos_a_serem_analisados = self.gerar_grafos_a_serem_analisados()
        dados_do_experimento = self.gerar_dados_do_experimento(grafos_a_serem_analisados)
        self.persistir_dados_do_experimento(dados_do_experimento)
        print "Experimento Concluído"
        print "Tabela de resultados salva em " + self.diretorio_do_resultado + '\\' + self.tabela_de_resultados.obter_titulo()  + '.csv'
        tempo_final = time.time()
        print "Tempo total: " + str(tempo_final - tempo_inicial)

    @abstractmethod
    def gerar_grafos_a_serem_analisados(self):
        raise NotImplementedError()

    def gerar_dados_do_experimento(self, grafos_a_serem_analisados):
        dados_do_experimento = []
        for grafo in grafos_a_serem_analisados:
            tempo_inicial = time.time()
            print "Analisando grafo ", grafo.obter_nome()
            dados_do_experimento.append(self.obter_dados_de_grafo(grafo))
            tempo_final = time.time()
            print "Tempo de analise, " + str(tempo_final - tempo_inicial)
        return dados_do_experimento

    @abstractmethod
    def obter_dados_de_grafo(self, grafo):
        raise NotImplementedError()

    def persistir_dados_do_experimento(self, dados_do_experimento):
        self.tabela_de_resultados = self.criar_tabela_de_resultados(dados_do_experimento)
        self.diretorio_do_resultado = self.formatar_diretorio_de_resultados()
        EscritorDeDados().escrever_objeto_tabela_em_arquivo_csv(self.tabela_de_resultados, self.diretorio_do_resultado)
        self.plotar_grafos_em_diretorio(dados_do_experimento)

    @abstractmethod
    def criar_tabela_de_resultados(self, dados_do_experimento):
        raise NotImplementedError()

    @abstractmethod
    def plotar_grafos_em_diretorio(self, dados_do_experimento):
        raise NotImplementedError()

    def executar_heuristica(self, grafo_original, algoritmo_de_heuristica):
        novo_grafo = grafo_original.copia()
        gerador_de_heuristica = GeradorDeHeuristica(algoritmo_de_heuristica)
        aresta_candidata = gerador_de_heuristica.estimar_aresta_de_maior_aumento_da_conectividade_algebrica(novo_grafo)
        return aresta_candidata

    def formatar_diretorio_de_resultados(self):
        return self.diretorio_do_resultado + "\\" + self.tabela_de_resultados.obter_titulo()