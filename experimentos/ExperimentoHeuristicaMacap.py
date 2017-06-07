from GeradorDeGrafos import GeradorDeGrafos
from AlgoritmoHeuristicaDePerturbacao import AlgoritmoHeuristicaDePerturbacao
from AlgoritmoHeuristicaDeExcentricidadeEGrau import AlgoritmoHeuristicaDeExcentricidadeEGrau
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from GeradorDeHeuristica import GeradorDeHeuristica
from Tabela import Tabela
from EscritorDeDados import EscritorDeDados
import time

class ExperimentoHeuristicaMacap:
    def __init__(self, diametro, ordem_minima, ordem_maxima):
        self.lista_de_grafos = []
        self.resultados = []
        self.diametro = diametro
        self.ordem_minima = ordem_minima
        self.ordem_maxima = ordem_maxima
        self.fixar_k = True
        titulo_da_tabela = "Resultados brooms, variando D de 86 a 100"
        if self.fixar_k:
            titulo_da_tabela += "k=1"
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
                                            "Aresta FB",
                                            "Conectividade Aumentada FB",
                                            "Melhor Heuristica"],
                                             titulo_da_tabela)

    def executar(self):
        self.lista_de_grafos = self.gerar_grafos_experimento_c()

        for grafo in self.lista_de_grafos:
            tempo_inicial = time.time()
            print "Analisando grafo ", grafo.obter_nome()
            self.efetuar_experimento_para_grafo(grafo)
            tempo_final = time.time()
            print "Tempo de analise, " + str(tempo_final - tempo_inicial)

        self.persistir_dados()

    def gerar_grafos(self):
        if self.fixar_k:
            listas_de_grafos_por_ordem = GeradorDeGrafos().gerar_listas_de_double_brooms_por_diametro_variando_ordem_com_k_fixado(
                                                                                                                 self.ordem_minima,
                                                                                                                 self.ordem_maxima,
                                                                                                                 self.diametro,
                                                                                                                 k=1)
            return listas_de_grafos_por_ordem
        else:
            listas_de_grafos_por_ordem = GeradorDeGrafos().gerar_listas_de_double_brooms_por_diametro_variando_ordem(self.ordem_minima,
                                                                                                                     self.ordem_maxima,
                                                                                                                     self.diametro)
            lista_de_grafos = []
            for lista in listas_de_grafos_por_ordem:
                lista_de_grafos = lista_de_grafos + lista
            return lista_de_grafos

    def gerar_grafos_experimento_c(self):
        lista_de_grafos = []
        for diametro in range(86, 101):
            lista_de_grafos.append(GeradorDeGrafos().gerar_broom(diametro, 2 * diametro - 1))
            lista_de_grafos.append(GeradorDeGrafos().gerar_broom(diametro, 2 * diametro))
        return lista_de_grafos

    def efetuar_experimento_para_grafo(self, grafo):
        dicionario_de_resultados = self._gerar_dicionario_de_resultados_para_grafo(grafo)
        self._adicionar_linha_de_resultados(grafo, dicionario_de_resultados)

    def _gerar_dicionario_de_resultados_para_grafo(self, grafo):
        dicionario_de_resultados = {"grafo": grafo}
        dicionario_de_resultados["aresta_hp"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDePerturbacao())
        dicionario_de_resultados["novo_grafo_hp"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_hp"])

        dicionario_de_resultados["aresta_he"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDeExcentricidadeEGrau())
        dicionario_de_resultados["novo_grafo_he"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_he"])

        dicionario_de_resultados["aresta_fb"] = self._calcular_aresta_heuristica(grafo, AlgoritmoHeuristicaDeForcaBruta())
        dicionario_de_resultados["novo_grafo_fb"] = grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb"])
        return dicionario_de_resultados

    def _calcular_aresta_heuristica(self, grafo_original, algoritmo_de_heuristica):
        novo_grafo = grafo_original.copia()
        gerador_de_heuristica = GeradorDeHeuristica(algoritmo_de_heuristica)
        aresta_candidata = gerador_de_heuristica.estimar_aresta_de_maior_aumento_da_conectividade_algebrica(novo_grafo)
        return aresta_candidata

    def _adicionar_linha_de_resultados(self, grafo, dicionario_de_resultados):

        conectividade_hp = round(grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_hp"]).obter_conectividade_algebrica(), 7)
        conectividade_he = round(grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_he"]).obter_conectividade_algebrica(), 7)
        conectividade_fb = round(grafo.copia().obter_grafo_equivalente_com_aresta_adicionada(dicionario_de_resultados["aresta_fb"]).obter_conectividade_algebrica(), 7)
        linha = [grafo.obter_diametro(),
                 grafo.obter_ordem(),
                 grafo.obter_k(),
                 grafo.obter_l(),
                 grafo.obter_nome(),
                 round(grafo.obter_conectividade_algebrica(), 7),
                 self.formatar_aresta(dicionario_de_resultados["aresta_hp"]),
                 conectividade_hp,
                 self.formatar_aresta(dicionario_de_resultados["aresta_he"]),
                 conectividade_he,
                 self.formatar_aresta(dicionario_de_resultados["aresta_fb"]),
                 conectividade_fb]
        if conectividade_hp > conectividade_he:
            linha.append("HP")
        elif conectividade_he > conectividade_hp:
            linha.append("HE")
        else:
            linha.append("Iguais")
        self.tabela_de_resultados.adicionar_linha(linha)

    def formatar_aresta(self, aresta):
        return (aresta[0]+1, aresta[1]+1)

    def persistir_dados(self):
        EscritorDeDados().escrever_objeto_tabela_em_arquivo_csv(self.tabela_de_resultados, "Resultados\\ExperimentoE")