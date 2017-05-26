from GeradorDeGrafos import GeradorDeGrafos
from DesenhistaDeGrafos import DesenhistaDeGrafos
from Tabela import Tabela
from AlgoritmoHeuristicaDePerturbacao import AlgoritmoHeuristicaDePerturbacao
from AlgoritmoHeuristicaDeExcentricidadeEGrau import AlgoritmoHeuristicaDeExcentricidadeEGrau
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBrutaAlterado
from GeradorDeHeuristica import GeradorDeHeuristica
from ExperimentoHeuristicaMacap import ExperimentoHeuristicaMacap
from DescritorDeGrafos import Descritor_de_grafos
from EscritorDeDados import EscritorDeDados
import time

'''
O experimento D consiste em gerar todas as brooms possiveis, registrando em um arquivo txt
algumas propriedades destes grafos. O objetivo e verificar se existe alguma propriedade
nos grafos especiais (aqueles cuja melhor aresta nao incide no vertice de maior grau) que
difere dos demais grafos.
'''

class ExperimentoD:
    def __init__(self):
        self.ordem_minima = 3
        self.ordem_maxima = 30

    def gerar_grafos(self):
        lista_de_grafos = []
        for diametro in range(self.ordem_minima, self.ordem_maxima):
            lista_de_grafos.append(GeradorDeGrafos().gerar_caminho(diametro+1))
        return lista_de_grafos

    def executar(self):
        lista_de_grafos = self.gerar_grafos()
        texto_de_saida = self.obter_texto_de_saida(lista_de_grafos)
        self.persistir_dados(texto_de_saida)

    def obter_texto_de_saida(self, lista_de_grafos):
        descritor = Descritor_de_grafos()
        texto = ""
        for grafo in lista_de_grafos:
            melhor_aresta = AlgoritmoHeuristicaDeForcaBruta().executar_algoritmo(grafo)
            melhor_aresta = (melhor_aresta[0] + 1, melhor_aresta[1] + 1)
            texto += "Melhor Aresta: " + str(melhor_aresta) + '\n'
            texto += descritor.obter_lista_de_informacoes_do_grafo(grafo)
        return texto

    def persistir_dados(self, texto):
        EscritorDeDados().escrever_texto_em_arquivo_txt(texto, "teste.txt", "C:\Users\HP\Desktop\Anderson")



ExperimentoD().executar()