from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from Widget import Widget
import Tkinter as Tk

class Canvas(Widget):
    figura = None
    canvas = None
    container = None

    def __init__(self, pai, figura, posicao=Tk.TOP):
        Widget.__init__(self, pai, posicao)
        self.figura = figura
        self.construir()

    def atualizar_figura(self, figura):
        self.figura = figura
        self.atualizar()

    def construir(self):
        self.container = Tk.Frame(master=self.pai, height=100, width=100)
        self.container.pack(side=self.posicao)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.container)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=self.posicao, fill=Tk.BOTH)

    def atualizar(self):
        self.canvas.figure = self.figura
        self.canvas.show()