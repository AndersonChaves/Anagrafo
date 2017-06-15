# *-* coding:utf8 *-*

#Esta classe analisa informacoes sobre grafos starlike.

class AnalisadorDeGrafosStarlike:
    starlike = None
    quantidade_de_ramos = -1
    diametros_dos_ramos = []
    ramos = []
    informacoes_de_arestas = [[{}]]

    def __init__(self, starlike):
        self.starlike = starlike
        self.quantidade_de_ramos = starlike.obter_grau_maximo()
        self.diametros_dos_ramos = self.obter_diametros_dos_ramos()
        self.ramos = self.obter_ramos()
        self.inicializar_dicionarios_de_informacoes_de_arestas()

    def inicializar_dicionarios_de_informacoes_de_arestas(self):
        self.informacoes_de_arestas = []
        for i in range(self.starlike.obter_ordem()):
            self.informacoes_de_arestas.append([])
            for j in range(self.starlike.obter_ordem()):
                self.informacoes_de_arestas[i].append({})

    def obter_arestas_de_todos_os_tipos(self):
        possiveis_arestas = self.starlike.obter_grafo_complemento().obter_lista_de_arestas()
        self.gerar_informacoes_de_arestas(possiveis_arestas)
        possiveis_arestas = self.remover_arestas_de_mesmo_tipo(possiveis_arestas)

        return possiveis_arestas

    def obter_pares_de_arestas_de_todos_os_tipos(self):
        possiveis_arestas = self.starlike.obter_grafo_complemento().obter_lista_de_arestas()



    def remover_arestas_de_mesmo_tipo(self, lista_de_arestas):
        tipos_ja_identificados = []
        lista_de_arestas_filtrada = []
        for aresta in lista_de_arestas:
            a, b = aresta
            if self.informacoes_de_arestas[a][b]["codigo"] not in tipos_ja_identificados:
                lista_de_arestas_filtrada.append(aresta)
                tipos_ja_identificados.append(self.informacoes_de_arestas[a][b]["codigo"])
        return lista_de_arestas_filtrada

    def gerar_informacoes_de_arestas(self, lista_de_arestas):
        for aresta in lista_de_arestas:
            a, b = aresta
            if not "codigo" in self.informacoes_de_arestas[a][b]:
                self.informacoes_de_arestas[a][b]["codigo"] = self.gerar_codigo_da_aresta(aresta)

    def gerar_codigo_da_aresta(self, aresta):
        tipo = self.obter_tipo_da_aresta(aresta)
        v1, v2 = aresta
        ramo_1, pos1 = self.identificar_ramo_correspondente_a_vertice(v1)
        ramo_2, pos2 = self.identificar_ramo_correspondente_a_vertice(v2)

        if tipo == "a":
            diam_2 = len(self.obter_ramo_correspondente_a_vertice(v2)) - 1
            return tipo + " " + str(pos2) + " " + str(diam_2)
        else:
            diam_1 = len(ramo_1) - 1
            diam_2 = len(ramo_2) - 1
            return tipo + " " + str(pos1) + " " + str(diam_1) + \
                                str(pos2) + " " + str(diam_2)

    def obter_tipo_da_aresta(self, aresta):
        v1, v2 = aresta
        if v1 == 0:
            return "a"
        elif self.vertices_em_mesmo_ramo(v1, v2):
            return "b"
        else:
            return "c"

    def obter_diametros_dos_ramos(self):
        if self.diametros_dos_ramos <> []:
            return self.diametros_dos_ramos

        self.quantidade_de_ramos = 0
        self.diametros_dos_ramos = []
        laplaciana = self.starlike.obter_laplaciana()
        tamanho = 0
        for i in range(1, self.starlike.obter_ordem()):
            tamanho += 1
            if laplaciana[i][i] == 1:
                self.quantidade_de_ramos += 1
                self.diametros_dos_ramos.append(tamanho)
                tamanho = 0
        return self.diametros_dos_ramos


    def vertices_em_mesmo_ramo(self, v1, v2):
        r1 = self.obter_ramo_correspondente_a_vertice(v1)
        r2 = self.obter_ramo_correspondente_a_vertice(v2)
        return r1 == r2

    def obter_ramo_correspondente_a_vertice(self, vertice):
        return self.identificar_ramo_correspondente_a_vertice(vertice)[0]

    def obter_posicao_do_vertice_em_ramo(self, vertice):
        return self.identificar_ramo_correspondente_a_vertice(vertice)[1]

    def identificar_ramo_correspondente_a_vertice(self, vertice):
        for ramo in self.ramos:
            for i in range(len(ramo)):
                if ramo[i] == vertice:
                    return (ramo, i)
        return None

    def obter_possiveis_arestas_de_mesmo_ramo_de_todos_os_tipos(self):
        lista_de_possiveis_arestas = []
        diametros_analisados = []
        for ramo in self.ramos:
            diametro_do_ramo = len(ramo)
            if diametro_do_ramo not in diametros_analisados:
                lista_de_possiveis_arestas += self.obter_possiveis_arestas_em_ramo(ramo)
                diametros_analisados.append(diametro_do_ramo)
        return lista_de_possiveis_arestas

    def obter_ramos(self):
        lista_de_ramos = []
        i = 1
        while i < self.starlike.obter_ordem():
            ramo = self.obter_vertices_no_ramo(i)
            lista_de_ramos.append(ramo)
            i += len(ramo) - 1
        return lista_de_ramos

    def obter_possiveis_arestas_em_ramo(self, lista_de_vertices):
        lista = []
        quantidade_de_vertices = len(lista_de_vertices)
        for i in range(quantidade_de_vertices - 2):
            for j in range(i+2, quantidade_de_vertices):
                aresta = (lista_de_vertices[i], lista_de_vertices[j])
                lista.append(aresta)
        return lista

    def obter_vertices_no_ramo(self, segundo_vertice_do_ramo):
        lista_de_vertices_do_ramo = [0]
        lista_de_vertices_do_ramo.append(segundo_vertice_do_ramo)
        laplaciana = self.starlike.obter_laplaciana()
        i = int(segundo_vertice_do_ramo) + 1
        while laplaciana[i][i] != 1:
            lista_de_vertices_do_ramo.append(self.starlike.obter_lista_de_vertices()[i])
            i += 1
        lista_de_vertices_do_ramo.append(self.starlike.obter_lista_de_vertices()[i])
        return lista_de_vertices_do_ramo

    def obter_possiveis_arestas_de_todos_os_tipos_entre_ramos(self):
        ramos_alternativos = self.ramos[:]
        lista_de_possiveis_arestas = []
        for ramo in self.ramos:
            ramos_alternativos.remove(ramo)
            for ramo_alternativo in ramos_alternativos:
                lista_de_possiveis_arestas += self.obter_possiveis_arestas_entre_ramos(ramo, ramo_alternativo)
        return lista_de_possiveis_arestas

    def obter_possiveis_arestas_entre_ramos(self, ramo_1, ramo_2):
        lista = []
        ramo_1_sem_vertice_inicial = ramo_1[:]
        ramo_1_sem_vertice_inicial.remove(0)
        ramo_2_sem_vertice_inicial = ramo_2[:]
        ramo_2_sem_vertice_inicial.remove(0)
        for i in range(len(ramo_1_sem_vertice_inicial)):
            for j in range(len(ramo_2_sem_vertice_inicial)):
                aresta = (ramo_1_sem_vertice_inicial[i], ramo_2_sem_vertice_inicial[j])
                lista.append(aresta)
        return lista

