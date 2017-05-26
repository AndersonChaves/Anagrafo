# coding=UTF-8
import sys
from PyQt4 import QtGui, QtCore
from Ui_MainWindow import Ui_MainWindow

class FrmTelaPrincipal(QtGui.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnGerarTabela.clicked.connect(self.teste)
        self.resized.connect(self.AtualizarImagem)
        #self.ui.graphicsView.resizeEvent(self.teste)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(FrmTelaPrincipal, self).resizeEvent(event)

    def AtualizarImagem(self):
        #self.teste()
        grafo = self.obter_grafo_informado()

    #def obter_grafo_informado(self):
        #k = int(self.edt_folhas_k.get().strip())
        #l = int(self.edt_folhas_l.get().strip())
        #d = int(self.edt_diametro.get().strip())
        #if self.int_gerar_complemento.get() == 0:
        #    grafo = GeradorDeGrafos().gerar_arvore_t(k, l, d)

    def teste(self):
        path = "2.jpg"
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(path))
        scene = QtGui.QGraphicsScene()
        scene.addItem(item)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(scene.itemsBoundingRect())
        self.ui.graphicsView.update()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FrmTelaPrincipal()
    window.show()
    sys.exit(app.exec_())