import mod, widgets, json
from PyQt6 import QtCore, QtGui, QtWidgets, QtTest


class WindowManager(QtWidgets.QStackedWidget):
    _selectView:'ProfileSelectWindow'
    _detailsView:'DetailsWindow'
    
    def __init__(self, window:QtWidgets.QMainWindow):
        super().__init__(window) # Initialize QStackedWidget

        # configure window
        window.setObjectName("MainWindow")
        window.setWindowTitle("Mod Tracker")
        window.resize(1000, 500)

        # update window manager to fit the window
        self.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        window.setCentralWidget(self)

        # create select view
        self._selectView = ProfileSelectWindow(self._openDetailsView)
        self._selectView.setParent(self)
        self._selectView.setGeometry(QtCore.QRect(0, 0, 1920, 1080))

    def addProfile(self, newProfile:mod.ModProfile):
        self._selectView.addProfile(newProfile, False)  

    def _openDetailsView(self, profile:mod.ModProfile):
        self._detailsView = DetailsWindow(self._selectView.saveJson, profile.modList, profile.priorityList, profile.selectedVersion, self._closeDetailsView)
        self.addWidget(self._detailsView)
        self.setCurrentWidget(self._detailsView)
        self._selectView.hide()

    def _closeDetailsView(self):
        self.removeWidget(self._detailsView)
        self._detailsView.deleteLater()
        self._selectView.show()

class DetailsWindow(QtWidgets.QWidget):
    _modList:list[mod.Mod]
    _priorityList:list[mod.ModPriority]
    _selectedVersion:str
    _profile:mod.ModPriority
    
    # QWidget objects
    _modTable:widgets.ModTable
    _pieChart:widgets.PieChart
    _addModTextField:QtWidgets.QLineEdit
    _selectedVersionTextField:QtWidgets.QLineEdit
    _addModBtn:QtWidgets.QPushButton
    _refreshBtn:QtWidgets.QPushButton
    _selectedVersionLabel:QtWidgets.QLabel
    
    # Constructor. Creates window and runs functions to create widgets
    def __init__(self, savefunc = lambda:0, modList:list[mod.Mod] = [],
                 priorityList:list[mod.ModPriority] = [
                     mod.ModPriority("High Priority", 255, 85, 0),
                     mod.ModPriority("Low Priority", 255, 255, 0)],
                 selectedVersion:str = "1.21.5", onBackButtonClick = None):
        super().__init__()

        # assign variables
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self._onBackButtonClick = onBackButtonClick
        self.savefunc = savefunc
        
        self._pieChart = widgets.PieChart(self, self._modList, self._selectedVersion)
        self._modTable = widgets.ModTable(self, self._modList, self._priorityList,
                                              self._selectedVersion, self.reloadWidgets, self.savefunc)

        self._createAddModTextField()
        self._createAddModBtn()
        self._createSelectedVersionTextField()
        self._createRefreshBtn()
        self._createBackBtn()

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

    # creates the add mod text input field,
    # where the user can input the URL of the mod they want to add.
    def _createAddModTextField(self):
        self._addModTextField = QtWidgets.QLineEdit(parent=self)
        self._addModTextField.setGeometry(QtCore.QRect(0, 910, 800, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        self._addModTextField.setFont(font)
        self._addModTextField.setObjectName("addModTextField")
        self._addModTextField.setPlaceholderText("Enter mod URL here")

    # creates the add mod button
    # which the user can click to add the mod they've input into the add mod text field.
    def _createAddModBtn(self):
        self._addModBtn = QtWidgets.QPushButton(parent=self)
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

        self._selectedVersionLabel = QtWidgets.QLabel(parent=self)
        self._selectedVersionLabel.setGeometry(QtCore.QRect(1560, 10, 120, 50))
        self._selectedVersionLabel.setFont(font)
        self._selectedVersionLabel.setObjectName("selectedVersionLabel")
        self._selectedVersionLabel.setText("Selected Version:")

        self._selectedVersionTextField = QtWidgets.QLineEdit(parent=self)
        self._selectedVersionTextField.setGeometry(QtCore.QRect(1685, 10, 120, 50))
        self._selectedVersionTextField.setFont(font)
        self._selectedVersionTextField.setObjectName("selectedVersionTextField")
        self._selectedVersionTextField.setText(self._selectedVersion)

    # creates the refresh button
    # which the user can click to call the API again, as well as refresh the table and pie chart.
    def _createRefreshBtn(self):
        self._refreshBtn = QtWidgets.QPushButton(parent=self)
        self._refreshBtn.setGeometry(QtCore.QRect(1810, 10, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self._refreshBtn.setFont(font)
        self._refreshBtn.setObjectName("refreshBtn")
        self._refreshBtn.clicked.connect(self._refresh)
        self._refreshBtn.setText("⟳")

    def _createBackBtn(self):
        self._refreshBtn = QtWidgets.QPushButton(parent=self)
        self._refreshBtn.setGeometry(QtCore.QRect(1865, 10, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self._refreshBtn.setFont(font)
        self._refreshBtn.setObjectName("backBtn")
        self._refreshBtn.setText("x")
        if (self._onBackButtonClick is not None):
            self._refreshBtn.clicked.connect(self._onBackButtonClick)

    # Adds a mod to the profile. Triggered when the add mod button is clicked.
    def _addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self._addModTextField.text()  # this gets the input from the text field

        newMod = mod.Mod(url = inputString, modPriority=self._priorityList[0])
        self._modList.append(newMod)
        self.savefunc()
        self.reloadWidgets(reloadEverything=True)

    def _refresh(self):
        self._selectedVersion = self._selectedVersionTextField.text()
        print(self._selectedVersion)
        # refresh API
        for mod in self._modList:
            mod.refreshMod()

        self.reloadWidgets()
        self.savefunc()

        

class ProfileSelectWindow(QtWidgets.QWidget):
    _profileList:list[mod.ModProfile]
    _priorityList:list[mod.ModPriority]

    _profileWidgets:list[QtWidgets.QPushButton] = []
    _addProfileWidget:QtWidgets.QPushButton

    _widgetSize = 400 # size of the profile widget (width and height)
    _widgetSpacing = 35 # spacing between profile widgets
    _widgetsPerRow = 4 # number of profile widgets per row
    _maxWidgets = 8 # maximum number of profile widgets
    _numWidgets = 0 # current number of profile widgets
    _rowPadding = 30 # padding between the first row of profile widgets and the top of the window

    _titleFontSize = 24  # size of the profile widget's name text
    _subtitleFontSize = 20  # size of the rest of the text on a profile widget
    _plusSignFontSize = 32  # size of the plus sign on the add profile widget

    def __init__(self, onProfileClick, profileList:list[mod.ModProfile] = [], priorityList:list[mod.ModPriority] = []):
        super().__init__()  # Initialize QWidget
        self._onProfileClick = onProfileClick
        self._profileList = profileList
        self._priorityList = priorityList

        self._addProfileWidget = None

        # Create a grid layout for managing widgets
        self._layout = QtWidgets.QGridLayout()
        self._layout.setSpacing(self._widgetSpacing)
        self.setLayout(self._layout)

        self._createWidgetRows()

    def addProfile(self, newProfile:mod.ModProfile, promptModName = True):
        if promptModName:
            dialog = QtWidgets.QInputDialog(self)
            inputStr, okPressed = dialog.getText(self, "Create new mdd profile", "New mod profile name:")
            if okPressed and len(inputStr) > 0:
                newProfile.name = inputStr
                self._profileList.append(newProfile)
                self._createProfileWidget()
        else:
            self._profileList.append(newProfile)
            self._createProfileWidget()

    def _createWidgetRows(self):
        if (len(self._profileList) == 0):
            self._createAddProfileWidget()
        else:
            for profile in self._profileList:
                self._createProfileWidget()

    def _createProfileWidget(self):
        if (self._numWidgets >= self._maxWidgets):
            return

        # Create a profile widget, which is a button that will be used to open the profile
        profileWidget = QtWidgets.QPushButton()
        profileWidget.setFixedSize(self._widgetSize, self._widgetSize)

        # Connect _openDetailsView() to the underlying button
        profileWidget.clicked.connect(lambda checked, id = self._numWidgets: self._openDetailsView(id))

        # Prepare fonts
        titleFont = QtGui.QFont()
        titleFont.setPointSize(self._titleFontSize)
        titleFont.setBold(True)

        subtitleFont = QtGui.QFont()
        subtitleFont.setPointSize(self._subtitleFontSize)

        # Profile name label
        profileNameLabel = QtWidgets.QLabel(parent=profileWidget)
        profileNameLabel.setText(self._profileList[self._numWidgets].name)
        profileNameLabel.setFont(titleFont)
        profileNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        profileNameLabel.setGeometry(QtCore.QRect(10, 25, self._widgetSize - 20, 150))
        profileNameLabel.setWordWrap(True)

        # Mod count label
        numModsLabel = QtWidgets.QLabel(parent=profileWidget)
        numModsLabel.setText(f"{len(self._profileList[self._numWidgets].modList)} mods")
        numModsLabel.setFont(subtitleFont)
        numModsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        numModsLabel.setGeometry(QtCore.QRect(10, 215, self._widgetSize - 20, 30))

        # Readiness label
        readinessLabel = QtWidgets.QLabel(parent=profileWidget)
        readinessLabel.setText(f"{self._profileList[self._numWidgets].getPercentReady():.2f}% ready\nfor {self._profileList[self._numWidgets].selectedVersion}")
        readinessLabel.setFont(subtitleFont)
        readinessLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        readinessLabel.setGeometry(QtCore.QRect(10, 280, self._widgetSize - 20, 60))

        # Add to list of profile widgets
        self._profileWidgets.append(profileWidget)

        # Add the widget to the grid layout
        row = self._numWidgets // self._widgetsPerRow
        col = self._numWidgets % self._widgetsPerRow
        self._layout.addWidget(profileWidget, row, col)

        # Increment the widget count and create add profile widget
        self._numWidgets += 1
        self._createAddProfileWidget()

    def _createAddProfileWidget(self):

        if (self._numWidgets >= self._maxWidgets or self._numWidgets < len(self._profileList)):
            return

        if (self._addProfileWidget is not None):
            self._addProfileWidget.deleteLater()

        self._addProfileWidget = QtWidgets.QPushButton(text="+")
        self._addProfileWidget.setFixedSize(self._widgetSize, self._widgetSize)
        self._addProfileWidget.clicked.connect(lambda: self.addProfile(mod.ModProfile()))

        # Set font
        font = QtGui.QFont()
        font.setPointSize(self._titleFontSize)
        font.setBold(True)
        self._addProfileWidget.setFont(font)

        # Add the widget to the grid layout
        row = self._numWidgets // self._widgetsPerRow
        col = self._numWidgets % self._widgetsPerRow
        self._layout.addWidget(self._addProfileWidget, row, col)

    def saveJson(self, filename="mods.json"):
        with open(filename, "w") as f:
            json.dump([profile.createDict() for profile in self._profileList], f, indent=4)
        self._profileWidgets = []
        self._numWidgets = 0
        self._createWidgetRows()

    def _openDetailsView(self, profileNum: int):
        profile = self._profileList[profileNum]
        self._onProfileClick(profile)