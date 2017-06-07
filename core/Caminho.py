class Caminho:
    def __init__(self, lista_de_vertices):
        self.lista_de_vertices = lista_de_vertices
        self.tamanho = len(lista_de_vertices) - 1
        self.vertice_origem = lista_de_vertices[0]
        self.vertice_destino = lista_de_vertices[-1]