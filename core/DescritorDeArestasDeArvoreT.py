class DescritorDeArestasDeArvoreT:

    def __init__(self, arvore_t):
        self.arvore_t = arvore_t
        self._lista_de_possiveis_arestas = []

    def obter_arestas_de_todos_os_tipos(self):
        lista_de_arestas = []
        lista_de_arestas.append(self._obter_uma_aresta_entre_folha_k_e_pai_l())
        lista_de_arestas.append(self._obter_uma_aresta_entre_folha_l_e_pai_k())
        lista_de_arestas.append(self._obter_uma_aresta_entre_folhas_nao_irmas())
        if self.arvore_t.obter_k() > 1 or self.arvore_t.obter_l() > 1:
            lista_de_arestas.append(self._obter_uma_aresta_entre_folhas_irmas())
        if self.arvore_t.obter_diametro() > 3:
            lista_de_arestas.append(self._obter_uma_aresta_entre_dois_nos_pais())
            lista_de_arestas = lista_de_arestas + self.obter_todas_as_possiveis_arestas_para_vertices_intermediarios()
        return lista_de_arestas

    def obter_todas_as_possiveis_arestas_para_vertices_intermediarios(self):
        lista_de_possiveis_arestas = []
        ids_dos_vertices_intermediarios = self.arvore_t.obter_lista_de_ids_de_vertices_intermediarios()
        for id_vertice_intermediario in ids_dos_vertices_intermediarios:
            pos = ids_dos_vertices_intermediarios.index(id_vertice_intermediario) + 1
            lista = self.obter_todas_as_possiveis_arestas_para_vertice_intermediario(id_vertice_intermediario,
                                                                                     ids_dos_vertices_intermediarios[pos:])
            lista_de_possiveis_arestas = lista_de_possiveis_arestas + lista
        return lista_de_possiveis_arestas

    def obter_todas_as_possiveis_arestas_para_vertice_intermediario(self, id_vertice, ids_dos_vertices_intermediarios):
        lista_de_possiveis_arestas = []
        lista_de_possiveis_arestas.append((id_vertice, self.arvore_t.obter_id_de_uma_folha_k()))
        lista_de_possiveis_arestas.append((id_vertice, self.arvore_t.obter_id_de_uma_folha_l()))

        lista_de_ids_a_nao_considerar = [id_vertice-1, id_vertice, id_vertice + 1]
        for id in ids_dos_vertices_intermediarios:
            if not (id in lista_de_ids_a_nao_considerar):
                lista_de_possiveis_arestas.append((id_vertice, id))

        if not self._vertice_possui_conexao_com_vertice_pai_k(id_vertice):
            lista_de_possiveis_arestas.append((id_vertice, self.arvore_t.obter_id_vertice_pai_de_folhas_k()))

        if not self._vertice_possui_conexao_com_vertice_pai_l(id_vertice):
            lista_de_possiveis_arestas.append((id_vertice, self.arvore_t.obter_id_vertice_pai_de_folhas_l()))
        return lista_de_possiveis_arestas

    def _obter_uma_aresta_entre_folha_l_e_pai_k(self):
        return self.arvore_t.obter_ordem() - 1, self.arvore_t.obter_id_vertice_pai_de_folhas_k()

    def _obter_uma_aresta_entre_folha_k_e_pai_l(self):
        vertice_pai_l = self.arvore_t.obter_id_vertice_pai_de_folhas_l()
        return (0, vertice_pai_l)

    def _obter_uma_aresta_entre_folhas_irmas(self):
        if (self.arvore_t.obter_k() > 1):
            return 0, 1
        elif self.arvore_t.obter_l() > 1:
            return self.arvore_t.obter_ordem() - 1, self.arvore_t.obter_ordem() - 2
        else:
            raise Exception("A arvore nao possui folhas irmas", "")

    def _obter_uma_aresta_entre_folhas_nao_irmas(self):
        return (0, self.arvore_t.obter_ordem() - 1)

    def _obter_uma_aresta_entre_dois_nos_pais(self):
        return self.arvore_t.obter_id_vertice_pai_de_folhas_l(), self.arvore_t.obter_id_vertice_pai_de_folhas_k()

    def _obter_uma_aresta_entre_uma_folha_k_e_intermediario(self, posicao_intermediaria):
        diferenca_entre_k_e_l = self.arvore_t.obter_l - self.arvore_t.obter_k()
        quantidade_de_nos_intermediarios = self.arvore_t.obter_diametro() - 2 - diferenca_entre_k_e_l - 1
        if quantidade_de_nos_intermediarios < posicao_intermediaria:
            raise Exception("No intermediario requisitado nao existente")
        else:
            return (self.arvore_t.obter_id_vertice_pai_de_folhas_k() - 1,
                    self.arvore_t.obter_id_vertice_pai_de_folhas_k() + posicao_intermediaria)

    def _obter_uma_aresta_entre_uma_folha_l_e_intermediario(self, posicao_intermediaria):
        quantidade_de_nos_intermediarios = self.arvore_t.obter_quantidade_de_nos_intermediarios()
        if quantidade_de_nos_intermediarios < posicao_intermediaria:
            raise Exception("No intermediario requisitado nao existente")
        else:
            return (self.arvore_t.obter_id_vertice_pai_de_folhas_l() - posicao_intermediaria,
                    self.arvore_t.obter_id_vertice_pai_de_folhas_l() + 1)

    def _obter_aresta_entre_pai_k_e_intermediario(self, posicao_intermediaria):
        return (self.arvore_t.obter_id_vertice_pai_de_folhas_k(),
                self.arvore_t.obter_id_vertice_pai_de_folhas_k() + posicao_intermediaria)

    def _obter_aresta_pai_l_intermediario(self, posicao_intermediaria):
        return (self.arvore_t.obter_id_vertice_pai_de_folhas_l(),
                self.arvore_t.obter_id_vertice_pai_de_folhas_l() - posicao_intermediaria)

    def _vertice_possui_conexao_com_vertice_pai_k(self, id_vertice):
        return (id_vertice < self.arvore_t.obter_id_vertice_pai_de_folhas_k()) or \
               (id_vertice == self.arvore_t.obter_id_vertice_pai_de_folhas_k() + 1)

    def _vertice_possui_conexao_com_vertice_pai_l(self, id_vertice):
        return (id_vertice > self.arvore_t.obter_id_vertice_pai_de_folhas_l()) or \
               (id_vertice == self.arvore_t.obter_id_vertice_pai_de_folhas_l() - 1)
