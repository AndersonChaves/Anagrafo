# -*- coding: UTF-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from interface import FrmTelaPrincipal

app = QtGui.QApplication(sys.argv)
window = FrmTelaPrincipal()
window.show()
sys.exit(app.exec_())

#import core.utils.CalculoDeVetores
#from GeradorDeGrafos import GeradorDeGrafos

#core.utils.CalculoDeVetores.calcular_menor_gargalo(GeradorDeGrafos().gerar_arvore_t(2, 2, 3))