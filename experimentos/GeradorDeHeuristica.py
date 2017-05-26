class GeradorDeHeuristica:

    def __init__(self, algoritmo):
        self.algoritmo_de_heuristica = algoritmo

    def atribuir_algoritmo(self, algoritmo):
        self.algoritmo_de_heuristica = algoritmo

    def estimar_aresta_de_maior_aumento_da_conectividade_algebrica(self, grafo):
        return self.algoritmo_de_heuristica.executar_algoritmo(grafo)
