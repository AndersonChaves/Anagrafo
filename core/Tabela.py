class Tabela:
    def __init__(self, campos, titulo="tabela"):
        self.campos = campos
        self.linhas = []
        self.titulo = titulo

    def adicionar_linha(self, linha):
        self.linhas.append(linha)

    def obter_campos(self):
        return self.campos

    def obter_dados(self):
        return self.linhas

    def obter_titulo(self):
        return self.titulo
