from AlgoritmoDeHeuristicaDeConectividadeAlgebrica import AlgoritmoDeHeuristicaDeConectividadeAlgebrica
from DescritorDeArestasDeArvoreT import DescritorDeArestasDeArvoreT
from itertools import combinations

class AlgoritmoHeuristicaDeForcaBruta(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        maior_conectividade = -1
        melhor_aresta = (-1, -1)
        for aresta in arestas_complementares:
            nova_conectividade = grafo.copia().adicionar_aresta(aresta).obter_conectividade_algebrica()
            if nova_conectividade > maior_conectividade:
                maior_conectividade = nova_conectividade
                melhor_aresta = aresta
        return melhor_aresta

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Forca Bruta"

class AlgoritmoHeuristicaDeForcaBrutaParaMaisDeUmaAresta(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        maior_conectividade = -1
        melhor_conjunto_de_arestas = []
        for combinacao_de_arestas in combinations(arestas_complementares, 2):
            nova_conectividade = grafo.copia().adicionar_arestas(combinacao_de_arestas).obter_conectividade_algebrica()
            if nova_conectividade > maior_conectividade:
                maior_conectividade = nova_conectividade
                melhor_conjunto_de_arestas = combinacao_de_arestas
        return melhor_conjunto_de_arestas

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Forca Bruta para k >= 1"


class AlgoritmoHeuristicaDeForcaBrutaAlterado(AlgoritmoDeHeuristicaDeConectividadeAlgebrica):
    def _executar(self, grafo):
        arestas_complementares = DescritorDeArestasDeArvoreT(grafo).obter_arestas_de_todos_os_tipos()
        maior_conectividade = grafo.copia().adicionar_aresta(arestas_complementares[0]).obter_conectividade_algebrica()
        segunda_maior_conectividade = grafo.copia().adicionar_aresta(arestas_complementares[1]).obter_conectividade_algebrica()

        melhor_aresta = arestas_complementares.pop(0)
        segunda_melhor_aresta = arestas_complementares.pop(0)

        if maior_conectividade < segunda_maior_conectividade:
            maior_conectividade, segunda_maior_conectividade = segunda_maior_conectividade, maior_conectividade
            melhor_aresta, segunda_maior_conectividade = segunda_melhor_aresta, melhor_aresta

        for aresta in arestas_complementares:
            nova_conectividade = grafo.copia().adicionar_aresta(aresta).obter_conectividade_algebrica()
            if nova_conectividade > maior_conectividade:
                maior_conectividade, segunda_maior_conectividade = nova_conectividade, maior_conectividade
                melhor_aresta, segunda_melhor_aresta = aresta, melhor_aresta
            elif nova_conectividade > segunda_maior_conectividade:
                segunda_maior_conectividade = nova_conectividade
                segunda_melhor_aresta = aresta

        return segunda_melhor_aresta

    def atualizar_lista_de_melhores_arestas(self, lista_de_melhores_arestas, maior_conectividade,
                                            lista_de_maiores_conectividades, tolerancia):
        lista_de_melhores_arestas_atualizada = []
        lista_de_maiores_conectividades_atualizada = []
        for i in range(len(lista_de_melhores_arestas)):
            if maior_conectividade - lista_de_maiores_conectividades[i] <= tolerancia:
                lista_de_maiores_conectividades_atualizada.append(lista_de_maiores_conectividades[i])
                lista_de_melhores_arestas_atualizada.append(lista_de_melhores_arestas[i])
        return (lista_de_melhores_arestas_atualizada, lista_de_maiores_conectividades_atualizada)

    def obter_lista_de_melhores_arestas(self, grafo):
        tolerancia = 0.00009
        arestas_complementares = DescritorDeArestasDeArvoreT(grafo).obter_arestas_de_todos_os_tipos()

        maior_conectividade = grafo.copia().adicionar_aresta(arestas_complementares[0]).obter_conectividade_algebrica()
        melhor_aresta = arestas_complementares.pop(0)

        lista_de_melhores_arestas = [melhor_aresta]
        lista_de_melhores_conectividades = [maior_conectividade]
        for aresta in arestas_complementares:
            nova_conectividade = grafo.copia().adicionar_aresta(aresta).obter_conectividade_algebrica()
            if nova_conectividade > maior_conectividade:
                maior_conectividade = nova_conectividade
                melhor_aresta = aresta
                lista_de_melhores_arestas, lista_de_melhores_conectividades = self.atualizar_lista_de_melhores_arestas(
                                                                                     lista_de_melhores_arestas, maior_conectividade,
                                                                                     lista_de_melhores_conectividades,
                                                                                     tolerancia)
                lista_de_melhores_arestas.append(aresta)
                lista_de_melhores_conectividades.append(nova_conectividade)
            elif maior_conectividade - nova_conectividade <= tolerancia:
                lista_de_melhores_arestas.append(aresta)
                lista_de_melhores_conectividades.append(nova_conectividade)

        return (lista_de_melhores_arestas, lista_de_melhores_conectividades)

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Forca Bruta Alterado"

class AlgoritmoHeuristicaDeForcaBrutaStarlike():

    def _executar(self, grafo):
        arestas_complementares = grafo.obter_grafo_complemento().obter_lista_de_arestas()
        maior_conectividade = -1
        melhor_aresta = (-1, -1)
        for aresta in arestas_complementares:
            nova_conectividade = grafo.copia().adicionar_aresta(aresta).obter_conectividade_algebrica()
            if nova_conectividade > maior_conectividade:
                maior_conectividade = nova_conectividade
                melhor_aresta = aresta
        return melhor_aresta

    def obter_nome_do_algoritmo(self):
        return "Heuristica de Forca Bruta (Starlike)"