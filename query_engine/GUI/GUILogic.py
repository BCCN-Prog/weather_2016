from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import gui


class MainDialog(QDialog, gui.Ui_MainWindow):
	
    def __init__(self, parent = None):
        super(MainDialog, self).__init__ (parent)
#        self.ui = self.Ui_MainWindow(self)

    def RecentSelected(self):
        ListRecent = [self.tr('All'), self.tr('Rain Chance')]
        ui.ParametersList.clear()
        ui.ParametersList.addItems(ListRecent)
        
    def HistoricalSelected(self):
        ListHistorical = [self.tr('All'), self.tr('Temperature'), self.tr('Rainfall')]
        ui.ParametersList.clear()
        ui.ParametersList.addItems(ListHistorical)
        


app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = MainDialog()
ui.setupUi(MainWindow)
MainWindow.show()


QtCore.QObject.connect(ui.RecentFlag, QtCore.SIGNAL("clicked()"), ui.RecentSelected)
QtCore.QObject.connect(ui.HistoricalFlag, QtCore.SIGNAL("clicked()"), ui.HistoricalSelected)



sys.exit(app.exec_())
