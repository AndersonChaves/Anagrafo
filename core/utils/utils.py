import os
from math import pow
from math import factorial

def criar_diretorio_se_nao_existir(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

def formatar_aresta_para_exibicao(aresta):
    return (aresta[0] + 1, aresta[1] + 1)

def formatar_lista_de_arestas_para_exibicao(lista_de_arestas):
    lista_formatada = []
    for aresta in lista_de_arestas:
        lista_formatada.append(formatar_aresta_para_exibicao(aresta))
    return lista_formatada

def zero(valor, precisao = 12):
    if abs(valor) < pow(10, -precisao):
        return True
    else:
        return False

def quantidade_de_combinacoes(n, r):
    return (factorial(n) / factorial(n - r)) / factorial(r)

def quantidade_de_permutacoes(n, r):
    return (factorial(n) / factorial(n - r))