from Grafo import Grafo
from DescritorDeArestasDeArvoreDoubleBroom import DescritorDeArestasDeArvoreDoubleBroom

class DoubleBroom(Grafo):
    def __init__(self, grafo_nx, d, n, k, l, nome=""):
        Grafo.__init__(self, grafo_nx, nome)
        self.diametro = d
        self.n = n
        self.k = k
        self.l = l
        self.descritor_de_arestas = DescritorDeArestasDeArvoreDoubleBroom(self)

    def obter_lista_de_ids_de_vertices_intermediarios(self):
        lista_de_vertices_intermediarios = []
        for i in range(self.k + 1, self.n - self.l - 1):
            lista_de_vertices_intermediarios.append(i)
        return lista_de_vertices_intermediarios

    def obter_k(self):
        return self.k

    def obter_l(self):
        return self.l

    def obter_diametro(self):
        return self.diametro

    def obter_id_vertice_pai_de_folhas_k(self):
        return self.k

    def obter_id_vertice_pai_de_folhas_l(self):
        return (self.n - self.l) - 1

    def obter_id_de_uma_folha_k(self):
        if self.k <= 0:
            raise Exception("A arvore nao possui folhas k", "")
        else:
            return 0

    def obter_id_de_uma_folha_l(self):
        if self.l <= 0:
            raise Exception("A arvore nao possui folhas l", "")
        else:
            return self.n - 1

    def obter_quantidade_de_vertices_intermediarios(self):
        diferenca_entre_k_e_l = self.obter_l() - self.obter_k()
        return self.obter_diametro() - 2 - diferenca_entre_k_e_l - 1