from AlgoritmoDeHeuristicaDeConectividadeAlgebrica import AlgoritmoDeHeuristicaDeConectividadeAlgebrica

class AlgoritmoHeuristicaDeMenorDiametro(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        menor_diametro = 9999
        melhor_aresta = (-1, -1)
        for aresta in arestas_complementares:
            diametro = grafo.copia().adicionar_aresta(aresta).obter_diametro()
            if diametro < menor_diametro:
                menor_diametro = diametro
                melhor_aresta = aresta
        return melhor_aresta

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Menor Diametro"