import networkx as nx
import numpy
from itertools import combinations

def calcularVetorFiedlerNetworkx(grafo):
  return nx.fiedler_vector(grafo)


def posicaoDoSegundoMenorValorEmLista(listaDeNumeros):
    menorValor, segundoMenorValor = float('inf'), float('inf')
    p1 = 0
    p2 = 0
    for i in range(len(listaDeNumeros)):
        if listaDeNumeros[i] <= menorValor:
            menorValor, segundoMenorValor = listaDeNumeros[i], menorValor
            p1, p2 = i, p1
        elif listaDeNumeros[i] < segundoMenorValor:
            segundoMenorValor = listaDeNumeros[i]
            p2 = i
    return p2

def obter_segundo_menor_valor_em_lista(lista_de_numeros):
    return lista_de_numeros[posicaoDoSegundoMenorValorEmLista(lista_de_numeros)]

def calcularVetorFiedlerNumpy(grafo):
    eigenvalues, eigenvectors = numpy.linalg.eig(nx.laplacian_matrix(grafo).A)
    eigenvalues = eigenvalues.real
    posicaoVetor = posicaoDoSegundoMenorValorEmLista(eigenvalues)
    vetorFiedler = eigenvectors[:, posicaoVetor]
    for i in range(len(vetorFiedler)):
        vetorFiedler[i] = round(vetorFiedler[i], 8)
    return (vetorFiedler, eigenvalues[posicaoDoSegundoMenorValorEmLista(eigenvalues.real)])

def calcularVetoresFiedler(listaDeGrafos):
  F = []
  for grafo in listaDeGrafos:
    f = calcularVetorFiedlerNumpy(grafo)
    F.append(f)
  return F


def remover_elementos_de_lista(lista, elementos):
    lista_resultante = list(lista)
    for i in range(len(elementos)):
        lista_resultante.remove(elementos[i])
    return lista_resultante

def obter_todos_as_combinacoes_possiveis_de_tamanho(lista, tamanho):
    return combinations(lista, tamanho)

def obter_arestas_ligando_particoes(grafo, particao_a, particao_b):
    arestas = []
    for vertice_a in particao_a:
        for vertice_b in particao_b:
            if grafo.grafo_nx.has_edge(vertice_a, vertice_b):
                arestas.append((vertice_a, vertice_b))

    return arestas

def _calcular_valor_cheeger(grafo, particao_a, particao_b):
    delta_a = obter_arestas_ligando_particoes(grafo, particao_a, particao_b)
    valor_cheeger = float(len(delta_a)) / float(len(particao_a))
    return valor_cheeger


def calcular_parametros_isoperimetricos(grafo):
    print "Calculando numero isoperimetrico", grafo.obter_nome()
    lista = grafo.grafo_nx.nodes()
    menor_valor_cheeger = 999999
    particao_a_resultante = lista
    particao_b_resultante = []
    for cardinalidade in range(0, len(lista) / 2):
        cardinalidade += 1
        for combinacao in combinations(lista, cardinalidade):
            particao_a = combinacao
            particao_b = remover_elementos_de_lista(lista, particao_a)
            valor_cheeger = _calcular_valor_cheeger(grafo, particao_a, particao_b)
            if valor_cheeger < menor_valor_cheeger:
                menor_valor_cheeger = valor_cheeger
                particao_a_resultante = particao_a
                particao_b_resultante = particao_b

    print menor_valor_cheeger, particao_a_resultante
    return ([particao_a_resultante, particao_b_resultante], menor_valor_cheeger)

def calcular_particionamento_isoperimetrico(grafo):
    particionamento, _ = calcular_parametros_isoperimetricos(grafo)
    return particionamento

def calcular_numero_isoperimetrico(grafo):
    _, resultado = calcular_parametros_isoperimetricos(grafo)
    return resultado

