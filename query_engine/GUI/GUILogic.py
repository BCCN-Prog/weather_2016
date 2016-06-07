from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

import gui

class MainDialog(QDialog, gui.Ui_MainWindow):
	
	def __init__(self, parent = None):
		super(MainDialog, self).__init__ (parent)
		self.setupUi(self)

app = QApplication(sys.argv)

#form = MainDialog()
#form.show()
#app.exec_() 

app = QtGui.QApplication(sys.argv)
form = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
