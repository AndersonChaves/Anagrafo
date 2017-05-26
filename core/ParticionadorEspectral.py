from EnumParticionamentoEspectral import EnumParticionamentoEspectral

class ParticionadorEspectral():

    def __init__(self, grafo_associado):
        self.grafo_associado = grafo_associado

    def vertices_na_mesma_particao(self, particionamento_do_grafo, id_no1, id_no2):
        return ((id_no1 in particionamento_do_grafo[0]) and (id_no2 in particionamento_do_grafo[0])
                or (id_no1 in particionamento_do_grafo[1]) and (id_no2 in particionamento_do_grafo[1]))

    def obter_particionamento_espectral_de_aresta(self, id_no1, id_no2):
        particionamento = self.grafo_associado.obter_particionamento_pelo_vetor_fiedler()
        if self.vertices_na_mesma_particao(particionamento, id_no1, id_no2):
            return EnumParticionamentoEspectral.POSITIVO_POSITIVO
        else:
            return EnumParticionamentoEspectral.POSITIVO_NEGATIVO


