from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import gui


class MainDialog(QDialog, gui.Ui_MainWindow):
	
    def __init__(self, parent = None):
        super(MainDialog, self).__init__ (parent)
        

    def RecentSelected(self):
        #ListRecent = [self.tr('All'), self.tr('Rain Chance')]
        ListRecent = ['All','Rain Chance']
        ui.ParametersList.clear()
        ui.ParametersList.addItems(ListRecent)
        
    def HistoricalSelected(self):
        #ListHistorical = [self.tr('All'), self.tr('Temperature'), self.tr('Rainfall')]
        ListHistorical = ['All','Temperature','Rainfall']
        ui.ParametersList.clear()
        ui.ParametersList.addItems(ListHistorical)
    
    def station_selected(self):
        print(self.StationsList.currentText())


app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = MainDialog()
ui.setupUi(MainWindow)
MainWindow.show()

ui.StationsList.currentIndexChanged.connect(ui.station_selected)
QtCore.QObject.connect(ui.RecentFlag, QtCore.SIGNAL("clicked()"), ui.RecentSelected)
QtCore.QObject.connect(ui.HistoricalFlag, QtCore.SIGNAL("clicked()"), ui.HistoricalSelected)

sys.exit(app.exec_())
