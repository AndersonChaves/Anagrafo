# -*- coding: UTF-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from interface import FrmTelaPrincipal


from TelaPrincipalTkinter import TelaPrincipalTkinter
from Tkinter import Tk

if __name__ == "__main__":
    raiz = Tk()
    TelaPrincipalTkinter(raiz)
    raiz.mainloop()



#app = QtGui.QApplication(sys.argv)
#window = FrmTelaPrincipal()
#window.show()
#sys.exit(app.exec_())

#import core.utils.CalculoDeVetores
#from GeradorDeGrafos import GeradorDeGrafos

#core.utils.CalculoDeVetores.calcular_menor_gargalo(GeradorDeGrafos().gerar_double_broom(2, 2, 3))