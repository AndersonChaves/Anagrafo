from Grafo import Grafo

#Classe para grafos Starlike de tipo 1: starlikes do tipo T(n, n, ..., n)
#NAO CONCLUIDA

class StarlikeTipo1(Grafo):
    tamanhos_dos_ramos = -1
    quantidade_de_ramos = -1

    def __init__(self, grafo_nx, nome=""):
        Grafo.__init__(self, grafo_nx, nome)
        self.tamanho_dos_ramos = self.obter_diametro() - 1
        self.quantidade_de_ramos = self.tamanho_dos_ramos

    def obter_arestas_de_todos_os_tipos(self):
        lista = self.obter_possiveis_arestas_no_caminho()
        lista = lista + self.obter_possiveis_arestas_entre_caminhos()
        return lista

    def obter_possiveis_arestas_no_caminho(self):
        lista = []
        t = self.tamanho_dos_ramos
        for i in range(t - 2):
            for j in range(i+2, t):
                lista.append((i, j))
        return lista

    def obter_possiveis_arestas_entre_caminhos(self):
        lista = []
        t = self.tamanho_dos_ramos
        for i in range(1, t):
            for j in range(t, 2*t-1):
                lista.append((i, j))
        return lista