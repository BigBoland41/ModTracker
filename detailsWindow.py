import mod, widgets
from PyQt6 import QtCore, QtGui, QtWidgets

class DetailsWindow(object):
    _modList:list[mod.Mod]
    _priorityList:list[mod.ModPriority]
    _selectedVersion:str
    _attemptErrorRecovery:bool
    
    _window:QtWidgets.QMainWindow
    _statusbar:QtWidgets.QStatusBar
    _modTable:widgets.ModTable
    _pieChart:widgets.PieChart
    _addModTextField:QtWidgets.QLineEdit
    _selectedVersionTextField:QtWidgets.QLineEdit
    _addModBtn:QtWidgets.QPushButton
    _refreshBtn:QtWidgets.QPushButton
    _selectedVersionLabel:QtWidgets.QLabel
    
    # Constructor. Creates window and runs functions to create widgets
    def __init__(self, window:QtWidgets.QMainWindow, modList:list[mod.Mod] = [],
                 priorityList:list[mod.ModPriority] = [
                     mod.ModPriority("High Priority", 255, 85, 0),
                     mod.ModPriority("Low Priority", 255, 255, 0)],
                 selectedVersion:str = "1.21.5", attemptErrorRecovery = True):
        # assign variables
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self._attemptErrorRecovery = attemptErrorRecovery

        # create app and window
        self._window = window
        self._configureWindow()
        
        self._pieChart = widgets.PieChart(self._window, self._modList, self._selectedVersion)
        self._modTable = widgets.ModTable(self._window, self._modList, self._priorityList,
                                              self._selectedVersion, self.reloadWidgets)

        self._createAddModTextField()
        self._createAddModBtn()
        self._createSelectedVersionTextField()
        self._createRefreshBtn()

    def loadNewData(self, modList:list[mod.Mod], priorityList:list[mod.ModPriority], selectedVersion:str):
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion

        self._modTable.loadNewData(self._modList, self._priorityList, self._selectedVersion)
        self._pieChart.loadNewData(self._modList, self._priorityList, self._selectedVersion)

    def reloadWidgets(self, rowNum = 0, reloadEverything = False):
        self._pieChart.loadChart(self._selectedVersion)
        if (reloadEverything):
            self._modTable.loadTable(self._selectedVersion)
        else:
            # self._modTable.reloadTableRow(rowNum)
            self._modTable.loadTable(self._selectedVersion) # required for tests to work properly

    # Getters
    def getModTable(self): return self._modTable
    
    def getPieChart(self): return self._pieChart

    def getModList(self): return self._modList
    
    def setAddModTextFieldText(self, text:str):
        self._addModTextField.setText(text)

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

    # creates the selected version text input field,
    # where the user can input the version of the game they want to check for.
    def _createSelectedVersionTextField(self):
        font = QtGui.QFont()
        font.setPointSize(12)

        self._selectedVersionLabel = QtWidgets.QLabel(parent=self._window)
        self._selectedVersionLabel.setGeometry(QtCore.QRect(1615, 10, 120, 50))
        self._selectedVersionLabel.setFont(font)
        self._selectedVersionLabel.setObjectName("selectedVersionLabel")
        self._selectedVersionLabel.setText("Selected Version:")

        self._selectedVersionTextField = QtWidgets.QLineEdit(parent=self._window)
        self._selectedVersionTextField.setGeometry(QtCore.QRect(1740, 10, 120, 50))
        self._selectedVersionTextField.setFont(font)
        self._selectedVersionTextField.setObjectName("selectedVersionTextField")
        self._selectedVersionTextField.setText(self._selectedVersion)

    # creates the refresh button
    # which the user can click to call the API again, as well as refresh the table and pie chart.
    def _createRefreshBtn(self):
        self._refreshBtn = QtWidgets.QPushButton(parent=self._window)
        self._refreshBtn.setGeometry(QtCore.QRect(1865, 10, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self._refreshBtn.setFont(font)
        self._refreshBtn.setObjectName("refreshBtn")
        self._refreshBtn.clicked.connect(self._refresh)
        self._refreshBtn.setText("⟳")

    # Adds a mod to the profile. Triggered when the add mod button is clicked.
    def _addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self._addModTextField.text()  # this gets the input from the text field

        newMod = mod.Mod(url = inputString, modPriority=self._priorityList[0])
        self._modList.append(newMod)
        self.reloadWidgets(reloadEverything=True)

    def _refresh(self):
        self._selectedVersion = self._selectedVersionTextField.text()

        # refresh API function goes here

        self.reloadWidgets()