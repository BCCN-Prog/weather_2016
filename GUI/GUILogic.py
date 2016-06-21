from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import gui
sys.path.append('../query_engine_v2')
from executor import get_data

ListRecentDaily = ['Parameter1','Parameter2']
ListRecentHourly = ['Parameter1','Parameter2']
ListHistoricalDaily = ['All','Maximum Temperature', 'Minimum Temperature', 'Average Temperature','Rain Chance', 'Rain Amount', 'Cloud Cover', 'Day']
ListHistoricalHourly = ['All','Temperature', 'Moisture', 'Cloud Cover', 'Rainfall', 'Rain Amount', 'Air Pressure reduced', 'Air Pressure Station', 'Windspeed' ]

class MainDialog(QDialog, gui.Ui_MainWindow):
	
    def __init__(self, parent = None):
        super(MainDialog, self).__init__ (parent)
        
    def Initialize_Connections(self):

        #ui.StationsList.currentIndexChanged.connect(ui.station_selected)
        QtCore.QObject.connect(ui.RecentFlag, QtCore.SIGNAL("clicked()"), ui.RecentSelected)
        QtCore.QObject.connect(ui.HistoricalFlag, QtCore.SIGNAL("clicked()"), ui.HistoricalSelected)

        QtCore.QObject.connect(ui.HourlyFlag, QtCore.SIGNAL("clicked()"), ui.HourlySelected)
        QtCore.QObject.connect(ui.DailyFlag, QtCore.SIGNAL("clicked()"), ui.DailySelected)
        ui.SubmitButton.released.connect(ui.Collect_Data)
        #ui.ExitButton.released.connect(QApplication.quit())
        #QtCore.QObject.connect(ui.ExitButton, SIGNAL(clicked()), SLOT(quit()))
    
    def Collect_Data(self):
        
        #Get Time
        StartingDateTime = str(ui.StartingDate.date().toPyDate())
        EndingDateTime = str(ui.EndingDate.date().toPyDate())
        StartingDateTime = StartingDateTime.replace('-','')
        EndingDateTime = EndingDateTime.replace('-','')
        
        if ui.HourlyFlag.isChecked():
            StartingTime = str(ui.StartingTime.time().toPyTime())
            EndingTime = str(ui.EndingTime.time().toPyTime())
            StartingDateTime += StartingTime[0:2]
            EndingDateTime += EndingTime[0:2]
        
            
        #Get h/d, r/h
        hourly_daily = ('h' if ui.HourlyFlag.isChecked() else 'd')
        recent_hist = ('h' if ui.HistoricalFlag.isChecked() else 'r')
        #get parameter and station (selected in drop-down menu)
        parameter = ui.ParametersList.currentText()
        station = ui.StationsList.currentText()
        get_data(hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime)
    def RecentSelected(self):
        if ui.HourlyFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListRecentHourly)
        elif ui.DailyFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListRecentDaily)

        
    def HistoricalSelected(self):
        if ui.DailyFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListHistoricalDaily)
        elif ui.HourlyFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListHistoricalHourly)

    def DailySelected(self):
        if ui.HistoricalFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListHistoricalDaily)
            ui.ParametersList.setEnabled(True)
        elif ui.RecentFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListRecentDaily)
            ui.ParametersList.setEnabled(True)
        ui.enable_stuff()
    def HourlySelected(self):
        if ui.HistoricalFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListHistoricalHourly)
        elif ui.RecentFlag.isChecked():
            ui.ParametersList.clear()
            ui.ParametersList.addItems(ListRecentHourly)
        ui.enable_stuff() 

    def enable_stuff(self):
            ui.ParametersList.setEnabled(True) 
            ui.StationsList.setEnabled(True) 
            ui.StartingDate.setEnabled(True) 
            ui.EndingDate.setEnabled(True) 
            ui.StartingDateLabel.setEnabled(True)
            ui.EndingDateLabel.setEnabled(True)
            if ui.HourlyFlag.isChecked():
                ui.StartingTime.setEnabled(True)
                ui.EndingTime.setEnabled(True)
            elif ui.DailyFlag.isChecked():
                ui.StartingTime.setEnabled(False)
                ui.EndingTime.setEnabled(False)                


app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = MainDialog()
ui.setupUi(MainWindow)
ui.Initialize_Connections()
MainWindow.show()

sys.exit(app.exec_())
