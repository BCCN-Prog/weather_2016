# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(360, 639)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 200, 250, 61))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.IntervalType = QtGui.QLabel(self.verticalLayoutWidget)
        self.IntervalType.setObjectName(_fromUtf8("IntervalType"))
        self.verticalLayout.addWidget(self.IntervalType)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.HourlyFlag = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.HourlyFlag.setEnabled(False)
        self.HourlyFlag.setObjectName(_fromUtf8("HourlyFlag"))
        self.horizontalLayout.addWidget(self.HourlyFlag)
        self.DailyFlag = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.DailyFlag.setEnabled(False)
        self.DailyFlag.setObjectName(_fromUtf8("DailyFlag"))
        self.horizontalLayout.addWidget(self.DailyFlag)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(60, 131, 250, 61))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.DataHistoryType = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.DataHistoryType.setObjectName(_fromUtf8("DataHistoryType"))
        self.verticalLayout_2.addWidget(self.DataHistoryType)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.HistoricalFlag = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.HistoricalFlag.setObjectName(_fromUtf8("HistoricalFlag"))
        self.horizontalLayout_2.addWidget(self.HistoricalFlag)
        self.RecentFlag = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.RecentFlag.setObjectName(_fromUtf8("RecentFlag"))
        self.horizontalLayout_2.addWidget(self.RecentFlag)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(70, 343, 219, 61))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.IntervalType_2 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.IntervalType_2.setObjectName(_fromUtf8("IntervalType_2"))
        self.verticalLayout_3.addWidget(self.IntervalType_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.StationsList = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.StationsList.setEnabled(False)
        self.StationsList.setObjectName(_fromUtf8("StationsList"))
        self.StationsList.addItem(_fromUtf8(""))
        self.StationsList.addItem(_fromUtf8(""))
        self.StationsList.addItem(_fromUtf8(""))
        self.StationsList.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.StationsList)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayoutWidget_4 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setEnabled(True)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 425, 291, 71))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.StartingDateLabel = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.StartingDateLabel.setEnabled(False)
        self.StartingDateLabel.setObjectName(_fromUtf8("StartingDateLabel"))
        self.horizontalLayout_7.addWidget(self.StartingDateLabel)
        self.StartingDate = QtGui.QDateEdit(self.verticalLayoutWidget_4)
        self.StartingDate.setEnabled(False)
        self.StartingDate.setCalendarPopup(True)
        self.StartingDate.setObjectName(_fromUtf8("StartingDate"))
        self.horizontalLayout_7.addWidget(self.StartingDate)
        self.StartingTime = QtGui.QTimeEdit(self.verticalLayoutWidget_4)
        self.StartingTime.setEnabled(False)
        self.StartingTime.setObjectName(_fromUtf8("StartingTime"))
        self.horizontalLayout_7.addWidget(self.StartingTime)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.EndingDateLabel = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.EndingDateLabel.setEnabled(False)
        self.EndingDateLabel.setObjectName(_fromUtf8("EndingDateLabel"))
        self.horizontalLayout_8.addWidget(self.EndingDateLabel)
        self.EndingDate = QtGui.QDateEdit(self.verticalLayoutWidget_4)
        self.EndingDate.setEnabled(False)
        self.EndingDate.setCalendarPopup(True)
        self.EndingDate.setObjectName(_fromUtf8("EndingDate"))
        self.horizontalLayout_8.addWidget(self.EndingDate)
        self.EndingTime = QtGui.QTimeEdit(self.verticalLayoutWidget_4)
        self.EndingTime.setEnabled(False)
        self.EndingTime.setObjectName(_fromUtf8("EndingTime"))
        self.horizontalLayout_8.addWidget(self.EndingTime)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_8)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayoutWidget_5 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(70, 272, 219, 61))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.IntervalType_3 = QtGui.QLabel(self.verticalLayoutWidget_5)
        self.IntervalType_3.setObjectName(_fromUtf8("IntervalType_3"))
        self.verticalLayout_6.addWidget(self.IntervalType_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.ParametersList = QtGui.QComboBox(self.verticalLayoutWidget_5)
        self.ParametersList.setEnabled(False)
        self.ParametersList.setObjectName(_fromUtf8("ParametersList"))
        self.ParametersList.addItem(_fromUtf8(""))
        self.ParametersList.addItem(_fromUtf8(""))
        self.ParametersList.addItem(_fromUtf8(""))
        self.ParametersList.addItem(_fromUtf8(""))
        self.horizontalLayout_6.addWidget(self.ParametersList)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.SubmitButton = QtGui.QPushButton(self.centralwidget)
        self.SubmitButton.setEnabled(False)
        self.SubmitButton.setGeometry(QtCore.QRect(60, 530, 98, 27))
        self.SubmitButton.setObjectName(_fromUtf8("SubmitButton"))
        self.ExitButton = QtGui.QPushButton(self.centralwidget)
        self.ExitButton.setGeometry(QtCore.QRect(180, 530, 98, 27))
        self.ExitButton.setObjectName(_fromUtf8("ExitButton"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 321, 101))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 54, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 127, 129))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 54, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 127, 129))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(248, 54, 57))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(161, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 0, 2))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 0, 4))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.textBrowser.setPalette(palette)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 41))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../Schreibtisch/weather.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 360, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuQuery_Engine = QtGui.QMenu(self.menubar)
        self.menuQuery_Engine.setObjectName(_fromUtf8("menuQuery_Engine"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuQuery_Engine.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.HistoricalFlag, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.HourlyFlag.setEnabled)
        QtCore.QObject.connect(self.HistoricalFlag, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.DailyFlag.setEnabled)
        QtCore.QObject.connect(self.RecentFlag, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.HourlyFlag.setEnabled)
        QtCore.QObject.connect(self.RecentFlag, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.DailyFlag.setEnabled)
        QtCore.QObject.connect(self.HourlyFlag, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.SubmitButton.setEnabled)
        QtCore.QObject.connect(self.DailyFlag, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.SubmitButton.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.HourlyFlag, self.DailyFlag)
        MainWindow.setTabOrder(self.DailyFlag, self.HistoricalFlag)
        MainWindow.setTabOrder(self.HistoricalFlag, self.RecentFlag)
        MainWindow.setTabOrder(self.RecentFlag, self.StationsList)
        MainWindow.setTabOrder(self.StationsList, self.StartingDate)
        MainWindow.setTabOrder(self.StartingDate, self.StartingTime)
        MainWindow.setTabOrder(self.StartingTime, self.EndingDate)
        MainWindow.setTabOrder(self.EndingDate, self.EndingTime)
        MainWindow.setTabOrder(self.EndingTime, self.ParametersList)
        MainWindow.setTabOrder(self.ParametersList, self.SubmitButton)
        MainWindow.setTabOrder(self.SubmitButton, self.ExitButton)
        MainWindow.setTabOrder(self.ExitButton, self.textBrowser)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Awesome Query Engine", None))
        self.IntervalType.setText(_translate("MainWindow", "Interval Type", None))
        self.HourlyFlag.setText(_translate("MainWindow", "Hourly", None))
        self.DailyFlag.setText(_translate("MainWindow", "Daily", None))
        self.DataHistoryType.setText(_translate("MainWindow", "Data Type", None))
        self.HistoricalFlag.setText(_translate("MainWindow", "Historical", None))
        self.RecentFlag.setText(_translate("MainWindow", "Recent", None))
        self.IntervalType_2.setText(_translate("MainWindow", "Stations", None))
        self.StationsList.setItemText(0, _translate("MainWindow", "All", None))
        self.StationsList.setItemText(1, _translate("MainWindow", "Berlin", None))
        self.StationsList.setItemText(2, _translate("MainWindow", "Hamburg", None))
        self.StationsList.setItemText(3, _translate("MainWindow", "Munich", None))
        self.StartingDateLabel.setText(_translate("MainWindow", "Starting Date", None))
        self.StartingTime.setDisplayFormat(_translate("MainWindow", "HH", None))
        self.EndingDateLabel.setText(_translate("MainWindow", "Ending Date  ", None))
        self.EndingTime.setDisplayFormat(_translate("MainWindow", "HH", None))
        self.IntervalType_3.setText(_translate("MainWindow", "Parameters", None))
        self.ParametersList.setItemText(0, _translate("MainWindow", "All", None))
        self.ParametersList.setItemText(1, _translate("MainWindow", "Berlin", None))
        self.ParametersList.setItemText(2, _translate("MainWindow", "Hamburg", None))
        self.ParametersList.setItemText(3, _translate("MainWindow", "Munich", None))
        self.SubmitButton.setText(_translate("MainWindow", "Submit", None))
        self.ExitButton.setText(_translate("MainWindow", "Exit", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Welcome to BCCN\'s </p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Awesome Weather App!</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">State your desires and we\'ll se what you can do for you</p></body></html>", None))
        self.menuQuery_Engine.setTitle(_translate("MainWindow", "Query Engine", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

