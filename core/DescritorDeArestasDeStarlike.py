class DescritorDeArestasDeStarlike:

    def __init__(self, starlike):
        self.starlike = starlike
        self._lista_de_possiveis_arestas = []

    def obter_arestas_de_todos_os_tipos(self):
        lista_de_arestas = []

        lista_de_arestas.append(self._obter_uma_aresta_entre_folha_k_e_pai_l())
        lista_de_arestas.append(self._obter_uma_aresta_entre_folha_l_e_pai_k())
        lista_de_arestas.append(self._obter_uma_aresta_entre_folhas_nao_irmas())
        if self.starlike.obter_k() > 1 or self.starlike.obter_l() > 1:
            lista_de_arestas.append(self._obter_uma_aresta_entre_folhas_irmas())
        if self.starlike.obter_diametro() > 3:
            lista_de_arestas.append(self._obter_uma_aresta_entre_dois_nos_pais())
            lista_de_arestas = lista_de_arestas + self.obter_todas_as_possiveis_arestas_para_vertices_intermediarios()
        return lista_de_arestas

