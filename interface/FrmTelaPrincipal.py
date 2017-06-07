# coding=UTF-8
import sys, os
from PyQt4 import QtGui, QtCore
from Ui_MainWindow import Ui_MainWindow
#from core import GeradorDeGrafos, DesenhistaDeGrafos
from core.GeradorDeGrafos import GeradorDeGrafos
from core.DesenhistaDeGrafos import DesenhistaDeGrafos
from core.DescritorDeGrafos import Descritor_de_grafos
from AlgoritmoHeuristicaDeForcaBruta import AlgoritmoHeuristicaDeForcaBruta
from AlgoritmoHeuristicaIsoperimetrica import AlgoritmoHeuristicaIsoperimetrica
#from ExperimentoE import ExperimentoE
#from ExperimentoF import ExperimentoF
#from ExperimentoG import ExperimentoG
from ExperimentoH import ExperimentoH
#from ExperimentoTeste import ExperimentoTeste

from ast import literal_eval as make_tuple

class FrmTelaPrincipal(QtGui.QMainWindow):
    resized = QtCore.pyqtSignal()
    grafo_exibido = None
    visualizacao_do_grafo = None
    experimento = ExperimentoH()

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.atribuir_parametros_iniciais()
        self.btnGerarGrafoClique()

    def atribuir_parametros_iniciais(self):
        self.ui.edtOrdem.setText("8")
        self.ui.edtDiametro.setText("5")
        self.ui.edtFolhas.setText("3")
        self.ui.btnGerarGrafo.clicked.connect(self.btnGerarGrafoClique)
        self.ui.btnGerarTabela.clicked.connect(self.efetuar_experimento)
        self.ui.btnAdicionarAresta.clicked.connect(self.adicionar_aresta)
        self.resized.connect(self.atualizar_imagem)

    def btnGerarGrafoClique(self):
        self.atualizar_dados_exibidos()

    def atualizar_dados_exibidos(self):
        self.atualizar_grafo()
        self.atualizar_visualizacao()
        self.atualizar_memo()

    def atualizar_grafo(self):
        self.grafo_exibido = self.obter_grafo_informado()

    def obter_grafo_informado(self):
        n = int(str(self.ui.edtOrdem.text()).strip())
        k = int(str(self.ui.edtFolhas.text()).strip())
        d = int(str(self.ui.edtDiametro.text()).strip())
        l = n - k - (d - 1)
        return GeradorDeGrafos().gerar_double_broom(k, l, d)
        #return GeradorDeGrafos().gerar_starlike([5, 5, 5, 5])

    def atualizar_visualizacao(self):
        if self.visualizacao_do_grafo != None:
            self.visualizacao_do_grafo.clf()
        self.visualizacao_do_grafo = self.gerar_visualizacao_do_grafo()
        self.atualizar_imagem()

    def gerar_visualizacao_do_grafo(self):
        return self.gerar_visualizacao_do_grafo_segundo_vetor_fiedler()
        #return self.gerar_visualizacao_do_grafo_de_acordo_com_numero_isoperimetrico()

    def gerar_visualizacao_do_grafo_segundo_vetor_fiedler(self):
        return DesenhistaDeGrafos().obter_grafo_plotado_de_acordo_com_vetor_fiedler(self.grafo_exibido)

    def atualizar_imagem(self):
        self.visualizacao_do_grafo.savefig('visualizacao')
        pixmap = QtGui.QPixmap('visualizacao.png')
        item = QtGui.QGraphicsPixmapItem(pixmap)
        scene = QtGui.QGraphicsScene()
        scene.addItem(item)
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(scene.itemsBoundingRect())
        self.ui.graphicsView.update()

    def gerar_visualizacao_do_grafo_de_acordo_com_numero_isoperimetrico(self):
        melhor_aresta = AlgoritmoHeuristicaDeForcaBruta().executar_algoritmo(self.grafo_exibido)
        grafo_com_arestas_adicionais = self.grafo_exibido.copia().obter_grafo_equivalente_com_aresta_adicionada(melhor_aresta)
        arestas_cheeger = AlgoritmoHeuristicaIsoperimetrica().executar_algoritmo(self.grafo_exibido)
        for aresta in arestas_cheeger:
            grafo_com_arestas_adicionais.obter_grafo_equivalente_com_aresta_adicionada(aresta)
        return DesenhistaDeGrafos().obter_grafo_plotado_de_acordo_com_numero_isoperimetrico(
            grafo_com_arestas_adicionais, [melhor_aresta, arestas_cheeger])

    def atualizar_memo(self):
        self.ui.textEdit.setText(Descritor_de_grafos(self.grafo_exibido).gerar_memo_de_informacoes_do_grafo())

    def adicionar_aresta(self):
        aresta = make_tuple(str(self.ui.edtAdicionarAresta.text()).strip())
        aresta = (aresta[0] - 1, aresta[1] - 1)
        self.grafo_exibido.obter_grafo_equivalente_com_aresta_adicionada(aresta)
        self.atualizar_memo()
        self.atualizar_visualizacao()
        self.resized.emit()

    def efetuar_experimento(self):
        if self.visualizacao_do_grafo != None:
            self.visualizacao_do_grafo.clf()
        self.experimento.executar_experimento()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(FrmTelaPrincipal, self).resizeEvent(event)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = FrmTelaPrincipal()
    window.show()
    window.resize(800, 600)
    sys.exit(app.exec_())