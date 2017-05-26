from AlgoritmoDeHeuristicaDeConectividadeAlgebrica import AlgoritmoDeHeuristicaDeConectividadeAlgebrica
import core.utils.CalculoDeVetores as CalculoDeVetores

class AlgoritmoHeuristicaIsoperimetrica(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        maior_cheeger = -1
        melhor_aresta = (-1, -1)
        for aresta in arestas_complementares:
            cheeger = CalculoDeVetores.calcular_numero_isoperimetrico(grafo.copia().adicionar_aresta(aresta))
            if cheeger > maior_cheeger:
                maior_cheeger = cheeger
                melhor_aresta = aresta
        return melhor_aresta

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Menor Diametro"