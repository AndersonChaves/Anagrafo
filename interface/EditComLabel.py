import Tkinter as Tk

class EditComLabel():
    pai = None
    mensagem = ""
    posicao = -1
    utilizar_spinner = False
    minimo = -1

    def __init__(self, pai, mensagem, posicao=Tk.TOP, utilizar_spinner=True, minimo=1):
        self.pai = pai
        self.mensagem = mensagem
        self.posicao = posicao
        self.utilizar_spinner = utilizar_spinner
        self.minimo = minimo
        self.construir()

    def construir(self):
        self.container = Tk.Frame(master=self.pai, height=5, width=5)
        self.container.pack(side=self.posicao)
        self.label = Tk.Label(self.container, text=self.mensagem)
        self.edit = Tk.Spinbox(master=self.container, from_=self.minimo, to=99, width=2)
        self.label.pack(side=Tk.LEFT)
        self.edit.pack(side=Tk.LEFT)

    def obter_valor_como_inteiro(self):
        return int(self.edit.get().strip())