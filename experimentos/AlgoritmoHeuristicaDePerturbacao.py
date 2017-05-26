from AlgoritmoDeHeuristicaDeConectividadeAlgebrica import AlgoritmoDeHeuristicaDeConectividadeAlgebrica


class AlgoritmoHeuristicaDePerturbacao(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        vetor_fiedler = grafo.obter_vetor_fiedler()
        aresta = self.obter_aresta_de_maior_diferenca_espectral(arestas_complementares, vetor_fiedler)
        return aresta

    def obter_aresta_de_maior_diferenca_espectral(self, lista_de_arestas, vetor_fiedler):
        maior_diferenca = -1
        aresta_candidata = []
        for aresta in lista_de_arestas:
            i, j = aresta
            if abs(vetor_fiedler[i] - vetor_fiedler[j]) > maior_diferenca:
                maior_diferenca = abs(vetor_fiedler[i] - vetor_fiedler[j])
                aresta_candidata = (i, j)

        if aresta_candidata[0] > aresta_candidata[1]:
            aresta_candidata = (aresta_candidata[1], aresta_candidata[0])

        return aresta_candidata

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Perturbacao"
