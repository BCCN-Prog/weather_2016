from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import gui
import pandas as pd
sys.path.append('../query_engine_v2')
import executor as ex


#Some Lists of stuff that the GUI should display
ListRecentDaily = ['Parameter1','Parameter2']
ListRecentHourly = ['Parameter1','Parameter2']
ListHistoricalDaily = ['Maximum Temperature', 'Minimum Temperature', 'Average Temperature', 'Rain Amount', 'Cloud Cover']
ListHistoricalHourly = ['Temperature', 'Moisture', 'Cloud Cover', 'Rainfall', 'Rain Amount', 'Air Pressure reduced', 'Air Pressure Station', 'Windspeed' ]
ListRecentDaily = ['Maximum Temperature', 'Minimum Temperature', 'Rain chance', 'Rain Amount','Air Pressure', 'Cloud Cover']
ListRecentHourly = ['Temperature', 'Humidity', 'Air Pressure', 'Windspeed', 'Rain Chance', 'Rain Amount', 'Cloud Cover']

StationTable = pd.read_table('stations.txt')
ListStations = StationTable['name'].tolist()


class MainDialog(QDialog, gui.Ui_MainWindow):
	
    def __init__(self, parent = None):
        '''
        Inherit all the shit from gui.ui, where the GUI architecture lies
        '''
        super(MainDialog, self).__init__ (parent)

        
    def Initialize_Connections(self):
        '''
        Tells the GUI which user actions (e.g. "RecentFlag[...]clicked()") should have which internal effect (e.g. set RecentSelected)
        '''
        
        QtCore.QObject.connect(ui.RecentFlag, QtCore.SIGNAL("clicked()"), ui.RecentSelected)
        QtCore.QObject.connect(ui.HistoricalFlag, QtCore.SIGNAL("clicked()"), ui.HistoricalSelected)

        QtCore.QObject.connect(ui.HourlyFlag, QtCore.SIGNAL("clicked()"), ui.HourlySelected)
        QtCore.QObject.connect(ui.DailyFlag, QtCore.SIGNAL("clicked()"), ui.DailySelected)
        ui.SubmitButton.released.connect(ui.Collect_Data)

    
    def Collect_Data(self):

        '''
        Most important part!
        When the user hits "submit", this function collects all data that were given as input, 
        initializes the Executor class which knows how to deal with this stuff further, 
        and calls the get_data function from executor, which will use smart_slice and visualization to create an output. 
        '''
        ###Run the other class###
        exec_ = ex.Executor()

        #Get Time
        StartingDateTime = str(ui.StartingDate.date().toPyDate())
        EndingDateTime = str(ui.EndingDate.date().toPyDate())
        StartingDateTime = StartingDateTime.replace('-','')
        EndingDateTime = EndingDateTime.replace('-','')
        StartingTime = 0
        EndingTime = 0
        if ui.HourlyFlag.isChecked():
            StartingTime = str(ui.StartingTime.time().toPyTime())
            EndingTime = str(ui.EndingTime.time().toPyTime())
            StartingTime = StartingTime[0:2]
            EndingTime = EndingTime[0:2]
        
        #Get hourly/daily, recent/hist
        hourly_daily = ('hourly' if ui.HourlyFlag.isChecked() else 'daily')
        recent_hist = ('historical' if ui.HistoricalFlag.isChecked() else 'recent')
        #Get parameter and station (selected in drop-down menu)
        parameter = ui.ParametersList.currentText()
        station = ui.StationsList.currentText()

        ###pass info!###
        exec_.get_data(hourly_daily, recent_hist, parameter, station, StartingDateTime, EndingDateTime, StartingTime, EndingTime)


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
            ui.StationsList.addItem("All")   
            ui.StationsList.addItems(ListStations)
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


### All this stuff will call the "MainDialog" class from gui.ui (the stuff that the graphical program created),
### initializes the gui and displays it. 

app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = MainDialog()
ui.setupUi(MainWindow)
ui.Initialize_Connections()
MainWindow.show()
sys.exit(app.exec_())
