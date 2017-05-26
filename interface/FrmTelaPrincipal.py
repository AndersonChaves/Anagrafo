# coding=UTF-8
import sys, os
from PyQt4 import QtGui, QtCore
from Ui_MainWindow import Ui_MainWindow
#from core import GeradorDeGrafos, DesenhistaDeGrafos
from core.GeradorDeGrafos import GeradorDeGrafos
from core.DesenhistaDeGrafos import DesenhistaDeGrafos
from core.DescritorDeGrafos import Descritor_de_grafos
from ExperimentoE import ExperimentoE
from ExperimentoF import ExperimentoF
from ast import literal_eval as make_tuple

class FrmTelaPrincipal(QtGui.QMainWindow):
    resized = QtCore.pyqtSignal()
    grafo_exibido = None
    img_grafo_original = None

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.edtOrdem.setText("8")
        self.ui.edtDiametro.setText("5")
        self.ui.edtFolhas.setText("3")
        self.gerar_grafo()
        self.ui.btnGerarGrafo.clicked.connect(self.gerar_grafo)
        self.ui.btnGerarTabela.clicked.connect(self.efetuar_experimento)
        self.ui.btnAdicionarAresta.clicked.connect(self.adicionar_aresta)
        #self.ui.cmbClasse.c
        self.resized.connect(self.AtualizarImagem)
        #self.resize(800, 600)

    def gerar_grafo(self):
        self.grafo_exibido = self.obter_grafo_informado()
        self.AtualizarImagem()
        self.atualizar_memo()

    def adicionar_aresta(self):
        aresta = make_tuple(str(self.ui.edtAdicionarAresta.text()).strip())
        aresta = (aresta[0] - 1, aresta[1] - 1)
        self.grafo_exibido.adicionar_aresta(aresta)
        self.atualizar_memo()
        self.AtualizarImagem()
        self.resized.emit()

    def atualizar_memo(self):
        self.ui.textEdit.setText(Descritor_de_grafos(self.grafo_exibido).obter_memo_de_informacoes_do_grafo())

    def resizeEvent(self, event):
        self.resized.emit()
        return super(FrmTelaPrincipal, self).resizeEvent(event)

    def AtualizarImagem(self):
        if self.img_grafo_original != None:
            self.img_grafo_original.clf()

        grafo_com_melhor_aresta = self.grafo_exibido.copia()
        from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
        melhor_aresta = AlgoritmoHeuristicaDeForcaBruta().executar_algoritmo(self.grafo_exibido)
        grafo_com_melhor_aresta.adicionar_aresta(melhor_aresta)

        from AlgoritmoHeuristicaIsoperimetrica import AlgoritmoHeuristicaIsoperimetrica
        aresta_cheeger = AlgoritmoHeuristicaIsoperimetrica().executar_algoritmo(self.grafo_exibido)
        grafo_com_melhor_aresta.adicionar_aresta(aresta_cheeger)

        self.img_grafo_original = DesenhistaDeGrafos().obter_grafo_plotado_de_acordo_com_numero_isoperimetrico(
            grafo_com_melhor_aresta, [melhor_aresta, aresta_cheeger])

        print 'arestas escolhidas: ', melhor_aresta, aresta_cheeger

        #self.img_grafo_original = DesenhistaDeGrafos().obter_grafo_plotado_de_acordo_com_vetor_fiedler(self.grafo_exibido)

        #self.img_grafo_original = DesenhistaDeGrafos().obter_grafo_plotado_de_acordo_com_numero_isoperimetrico(self.grafo_exibido)
        self.img_grafo_original.savefig('teste001')
        print self.grafo_exibido.obter_lista_de_arestas()
        pixmap = QtGui.QPixmap('teste001.png')
        item = QtGui.QGraphicsPixmapItem(pixmap)
        scene = QtGui.QGraphicsScene()
        scene.addItem(item)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(scene.itemsBoundingRect())
        self.ui.graphicsView.update()

    def obter_grafo_informado(self):
        n = int(str(self.ui.edtOrdem.text()).strip())
        k = int(str(self.ui.edtFolhas.text()).strip())
        d = int(str(self.ui.edtDiametro.text()).strip())
        l = n - k - (d - 1)
        return GeradorDeGrafos().gerar_arvore_t(k, l, d)

    def efetuar_experimento(self):
        print 'a'
        experimento = ExperimentoF()
        experimento.executar_experimento()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FrmTelaPrincipal()
    window.show()
    window.resize(800, 600)
    sys.exit(app.exec_())