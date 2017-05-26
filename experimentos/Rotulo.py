import Tkinter as Tk

class Rotulo:
    def __init__(self, frame, texto, posicao):
        self.frame = frame
        self.container = Tk.Frame(master=self.frame)
        self.string_de_controle = Tk.StringVar()
        self.string_de_controle.set(texto)
        self.label = Tk.Label(master=self.container, textvariable=self.string_de_controle)
        #self.label = Tk.Label(master=self.frame, textvariable=self.string_de_controle)
        #self.label = Tk.Label(master=self.frame)
        self.container.pack(side=posicao)
        self.label.pack(side=Tk.TOP)

    def alterar_texto(self, texto):
        self.string_de_controle.set(texto)

    def obter_texto(self):
        return self.string_de_controle.get()