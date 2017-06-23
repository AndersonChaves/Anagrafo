from Widget import Widget
import Tkinter as Tk

class Botao(Widget):
    posicao = Tk.LEFT

    def __init__(self, pai, mensagem, funcao, posicao=Tk.TOP):
        Widget.__init__(self, pai, posicao)
        self.mensagem = mensagem
        self.funcao = funcao
        self.construir()

    def construir(self):
        self.btn_gerar_grafo = Tk.Button(master=self.pai, text=self.mensagem,
                                         command=self.funcao, height=1, pady=1)
        self.btn_gerar_grafo.pack(side=self.posicao)