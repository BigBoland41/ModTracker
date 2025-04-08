import mod, widgets
from PyQt6 import QtCore, QtGui, QtWidgets

class DetailsWindow(object):
    _modList:list[mod.Mod]
    _priorityList:list[mod.ModPriority]
    
    _window:QtWidgets.QMainWindow
    _statusbar:QtWidgets.QStatusBar
    _modTable:widgets.ModTable
    _pieChart:widgets.PieChart
    
    # Constructor. Creates window and runs functions to create widgets
    def __init__(self, window:QtWidgets.QMainWindow, modList:list[mod.Mod] = [],
                 priorityList:list[mod.ModPriority] = [
                     mod.ModPriority("High Priority", 255, 85, 0),
                     mod.ModPriority("Low Priority", 255, 255, 0)],
                 selectedVersion:str = "1.21.5"):
        # assign variables
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion

        # create app and window
        self._window = window
        self._configureWindow()
        
        self._pieChart = widgets.PieChart(self._window, self._modList, self._selectedVersion)
        self._modTable = widgets.ModTable(self._window, self._modList, self._priorityList,
                                              self._selectedVersion, self.reloadWidgets)

        self._createAddModTextField()
        self._createAddModBtn()
        
    def reloadWidgets(self, rowNum = 0, reloadEverything = False):
        self._pieChart.loadChart()
        if (reloadEverything):
            self._modTable.loadTable()
        else:
            self._modTable.reloadTableRow(rowNum)

    # Getters
    def getModTable(self):
        return self._modTable
    
    def getPieChart(self):
        return self._pieChart
    
    def setAddModTextFieldText(self, text:str):
        self._addModTextField.setText(text)

    def clickAddModBtn(self):
        self._addModBtn.click()

    # configures the window, including name, size, and status bar
    def _configureWindow(self):
        self._window.setObjectName("MainWindow")
        self._window.setWindowTitle("Mod Tracker")
        self._window.resize(1000, 500)

        self._statusbar = QtWidgets.QStatusBar(parent=self._window)
        self._statusbar.setObjectName("statusbar")
        self._window.setStatusBar(self._statusbar)
        QtCore.QMetaObject.connectSlotsByName(self._window)

    # creates the add mod text input field,
    # where the user can input the URL of the mod they want to add.
    def _createAddModTextField(self):
        self._addModTextField = QtWidgets.QLineEdit(parent=self._window)
        self._addModTextField.setGeometry(QtCore.QRect(0, 910, 800, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        self._addModTextField.setFont(font)
        self._addModTextField.setObjectName("addModTextField")
        self._addModTextField.setText("Enter mod URL here")

    # creates the add mod button
    # which the user can click to add the mod they've input into the add mod text field.
    def _createAddModBtn(self):
        self._addModBtn = QtWidgets.QPushButton(parent=self._window)
        self._addModBtn.setGeometry(QtCore.QRect(800, 910, 200, 70))
        font = QtGui.QFont()
        font.setPointSize(18)
        self._addModBtn.setFont(font)
        self._addModBtn.setObjectName("addModBtn")
        self._addModBtn.clicked.connect(self._addMod)
        self._addModBtn.setText("Add Mod")

    # Adds a mod to the profile. Triggered when the add mod button is clicked.
    def _addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self._addModTextField.text()  # this gets the input from the text field

        newMod = mod.Mod(url = inputString, modPriority=self._priorityList[0])
        self._modList.append(newMod)
        self.reloadWidgets(reloadEverything=True)