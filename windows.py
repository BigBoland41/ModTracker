import mod, widgets
from PyQt6 import QtCore, QtGui, QtWidgets, QtTest

class DetailsWindow(object):
    _modList:list[mod.Mod]
    _priorityList:list[mod.ModPriority]
    _selectedVersion:str
    
    # QWidget objects
    _window:QtWidgets.QMainWindow
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

    def enterAndAddMod(self, modURL:str):
        self._addModTextField.setText("")
        QtTest.QTest.keyClicks(self._addModTextField, modURL)
        QtTest.QTest.mouseClick(self._addModBtn, QtCore.Qt.MouseButton.LeftButton)

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

    # creates the add mod text input field,
    # where the user can input the URL of the mod they want to add.
    def _createAddModTextField(self):
        self._addModTextField = QtWidgets.QLineEdit(parent=self._window)
        self._addModTextField.setGeometry(QtCore.QRect(0, 910, 800, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        self._addModTextField.setFont(font)
        self._addModTextField.setObjectName("addModTextField")
        self._addModTextField.setPlaceholderText("Enter mod URL here")

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
        self._modTable.saveModList()
        self.reloadWidgets(reloadEverything=True)

    def _refresh(self):
        self._selectedVersion = self._selectedVersionTextField.text()

        # refresh API function goes here
        for mod in self._modList:
            mod.refreshMod()
        self._modTable.saveModList()
        self.reloadWidgets()

class ProfileSelectWindow(object):
    _priorityList:list[mod.ModPriority]

    _window:QtWidgets.QMainWindow

    _widgetSize = 275 # size of the profile widget (width and height)
    _widgetSpacing = 35 # spacing between profile widgets
    _widgetsPerRow = 6 # number of profile widgets per row
    _maxWidgets = 17 # maximum number of profile widgets to create
    _rowPadding = 30 # padding between the first row of profile widgets and the top of the window

    def __init__(self, window:QtWidgets.QMainWindow, priorityList:list[mod.ModPriority] = []):
        self._window = window
        self._priorityList = priorityList

        self._configureWindow()
        self._createWidgetRows(19)

    def _configureWindow(self):
        self._window.setObjectName("MainWindow")
        self._window.setWindowTitle("Mod Tracker")
        self._window.resize(1000, 500)

    def _createWidgetRows(self, numWidgets:int):
        for i in range(numWidgets):
            self._createProfileWidget(i)

    def _createProfileWidget(self, numWidget:int):
        if (numWidget >= self._maxWidgets):
            return

        # create a profile widget, which is a button that will be used to open the profile
        profileWidget = QtWidgets.QPushButton(parent=self._window)

        # determine the how much to offset the first column (start of the first row) in order to center the widgets
        # in the window. This is done by calculating the total width of all widgets in a row and subtracting it from the window width.
        totalRowWidth = self._widgetsPerRow * self._widgetSize + (self._widgetsPerRow - 1) * self._widgetSpacing
        colPadding = (1920 - totalRowWidth) // 2

        profileWidget.setGeometry(QtCore.QRect(
            colPadding + (self._widgetSize + self._widgetSpacing) * (numWidget % self._widgetsPerRow),
            self._rowPadding + (self._widgetSize + self._widgetSpacing) * (int(numWidget / self._widgetsPerRow)),
            self._widgetSize,
            self._widgetSize
        ))

        # Prepare font sizes
        titleFont = QtGui.QFont()
        titleFont.setPointSize(24)
        subtitleFont = QtGui.QFont()
        subtitleFont.setPointSize(16)
        
        # Profile name label
        titleLabel = QtWidgets.QLabel(parent=profileWidget)
        titleLabel.setText("default")
        titleFont.setBold(True)
        titleLabel.setFont(titleFont)
        titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        titleLabel.setGeometry(QtCore.QRect(0, 25, self._widgetSize, 40))

        # Mod count label
        subtitleLabel1 = QtWidgets.QLabel(parent=profileWidget)
        subtitleLabel1.setText("23 mods")
        subtitleLabel1.setFont(subtitleFont)
        subtitleLabel1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        subtitleLabel1.setGeometry(QtCore.QRect(0, 115, self._widgetSize, 30))

        # Readiness label
        subtitleLabel2 = QtWidgets.QLabel(parent=profileWidget)
        subtitleLabel2.setText("88% ready\nfor 1.21.4")
        subtitleLabel2.setFont(subtitleFont)
        subtitleLabel2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        subtitleLabel2.setGeometry(QtCore.QRect(0, 180, self._widgetSize, 60))