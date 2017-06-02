from AlgoritmoDeHeuristicaDeConectividadeAlgebrica import AlgoritmoDeHeuristicaDeConectividadeAlgebrica
import core.utils.CalculoDeVetores as CalculoDeVetores

class AlgoritmoHeuristicaIsoperimetrica(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    melhor_aresta = (-1, -1)
    lista_de_melhores_arestas = []

    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        maior_cheeger = -1
        melhor_aresta = (-1, -1)
        lista_de_melhores_arestas = [melhor_aresta]

        for aresta in arestas_complementares:
            cheeger = CalculoDeVetores.calcular_numero_isoperimetrico(grafo.copia().adicionar_aresta(aresta))
            cheeger = round(cheeger, 10)
            if cheeger > maior_cheeger:
                maior_cheeger = cheeger
                lista_de_melhores_arestas = [aresta]
            elif cheeger == maior_cheeger:
                lista_de_melhores_arestas.append(aresta)

        self.lista_de_melhores_arestas = lista_de_melhores_arestas
        self.melhor_aresta = lista_de_melhores_arestas[0]

    def obter_melhor_aresta(self):
        return self.melhor_aresta

    def obter_lista_de_melhores_arestas(self):
        return self.lista_de_melhores_arestas

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Menor Diametro"