import mod, widgets, load, json, threading, os, readJarFile
from PyQt6 import QtCore, QtGui, QtWidgets, QtTest


# Manages the two primary displays in the main window, including communication and switching displays. Also manages the small loading window.
class WindowManager(QtWidgets.QStackedWidget):
    _selectView:'ProfileSelectWindow'
    _detailsView:'DetailsWindow'
    _loadingWindow:'LoadingWindow'
    
    def __init__(self, window:QtWidgets.QMainWindow, loadJson=True, openLoadingWindow=True, printLoadingText=True, processEventsFunc = lambda : 1+1):
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

        # load profile data from json file (if enabled). Create and open a LoadingWindow (if enabled)
        if loadJson:
            if openLoadingWindow:
                self._loadingWindow = LoadingWindow()
                self._loadingWindow.show()
                processEventsFunc()
            
            self._loadProfile(printLoadingText)

            if openLoadingWindow:
                self._loadingWindow.close()

    def _loadProfile(self, printLoadingText=True):
        if printLoadingText:
            print("Loading profiles...")

        # call create profile list and add the resulting data to the select view
        profiles = load.createProfileList()
        for profile in profiles:
            self._selectView.addProfile(profile, "New Profile", saveToFile=False)
        self._selectView.sortModLists()

    def _openDetailsView(self, profile:mod.ModProfile):
        self._detailsView = DetailsWindow(profile.modList, profile.priorityList, profile.selectedVersion, self._closeDetailsView, self._selectView.saveJson)
        self.addWidget(self._detailsView)
        self.setCurrentWidget(self._detailsView)
        self._selectView.hide()

    def _closeDetailsView(self):
        self.removeWidget(self._detailsView)
        self._detailsView.deleteLater()
        self._selectView.show()


# Temporary window to display while the app is starting
class LoadingWindow(QtWidgets.QWidget):
    _movie:QtGui.QMovie

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading")
        self.setFixedSize(300, 200)
        layout = QtWidgets.QVBoxLayout()

        # Add a QLabel for the GIF
        gif_label = QtWidgets.QLabel()
        gif_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Load and set the GIF
        self._movie = QtGui.QMovie("loading.gif")
        self._movie.setScaledSize(QtCore.QSize(150, 150))
        gif_label.setMovie(self._movie)
        self._movie.start()

        # Add a text label below the GIF
        text_label = QtWidgets.QLabel("Loading, please wait...")
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Add widgets to the layout
        layout.addWidget(gif_label)
        layout.addWidget(text_label)
        self.setLayout(layout)


# Small, customizable window that gives the user several options to choose from.
# Adds a button for each button label provided. Will only show a 
# MultipleChoiceWindow.exec() will return the number option chosen (1 indexed). If no option is chosen, it will return 0.
class MultipleChoiceWindow(QtWidgets.QDialog):
    buttonList = []
    inputField = None

    def __init__(
            self,
            button_labels = ["Option 1", "Option 2", "Option 3"],

            parent=None,
            windowTitle="Select an option",

            button_width=250,
            button_height=40,
            button_fontSize=12,

            showLabel=False,
            label_text="Select an option",
            label_fontSize = 14,
            
            showTextInput = False,
            textInput_labelText = "Enter Text:",
            textInput_placeholderText = "Enter Text Here"
    ):
        super().__init__(parent)
        self.setWindowTitle(windowTitle)
        self.setModal(True)

        self.layout = QtWidgets.QVBoxLayout(self)

        if showLabel:
            label = widgets.createLabel(labelText=label_text, fontSize=label_fontSize, bold=True, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(label)

        if showTextInput:
            inputField_label = widgets.createLabel(labelText=textInput_labelText)
            self.inputField = widgets.createTextField(placeholderText=textInput_placeholderText)

            self.layout.addWidget(inputField_label)
            self.layout.addWidget(self.inputField)

        for i, inputField_label in enumerate(button_labels):
            button = widgets.createButton(btnText=inputField_label, fontSize=button_fontSize, minimumWidth=button_width, minimumHeight=button_height)
            self.buttonList.append(button)
            self.layout.addWidget(button)
            button.clicked.connect(lambda checked=False, idx=i + 1: self.done(idx))
    
    def getInputFieldText(self):
        if self.inputField:
            return self.inputField.text()
        else:
            return None


# The display that shows the user a detailed view of a specific mod profile and allows them to manipulate it
class DetailsWindow(QtWidgets.QWidget):
    # Parameters
    _modList:list[mod.Mod]
    _priorityList:list[mod.ModPriority]
    _selectedVersion:str
    
    # Complex Widgets
    _modTable:widgets.ModTable_Manager
    _pieChart:widgets.PieChart
    _modLoaderDropdown:widgets.ModLoaderDropdownBtn

    # Buttons
    _addModBtn:QtWidgets.QPushButton
    _refreshBtn:QtWidgets.QPushButton
    _exportBtn:QtWidgets.QPushButton
    _backBtn:QtWidgets.QPushButton
    _downloadBtn:QtWidgets.QPushButton

    # Labels and Text Fields
    _addModTextField:QtWidgets.QLineEdit
    _selectedVersionLabel:QtWidgets.QLabel
    _selectedVersionTextField:QtWidgets.QLineEdit
    _errorLabel:QtWidgets.QLabel
    
    # Constructor. Creates window and runs functions to create widgets
    def __init__(self, modList:list[mod.Mod] = [],
                 priorityList:list[mod.ModPriority] = [
                     mod.ModPriority("High Priority", 255, 85, 0),
                     mod.ModPriority("Low Priority", 255, 255, 0)],
                 selectedVersion:str = "1.21.5",
                 onBackButtonClick = None,
                 savefunc = None):
        super().__init__()

        # assign variables
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self._onBackBtnClick = onBackButtonClick
        self._savefunc = savefunc

        self._createWidgets()

    # Inserts new data to diplay instead. Used for testing.
    def loadNewData(self, modList:list[mod.Mod], priorityList:list[mod.ModPriority], selectedVersion:str):
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion

        self._modTable.loadNewData(self._modList, self._priorityList, self._selectedVersion)
        self._pieChart.loadNewData(self._modList, self._priorityList, self._selectedVersion)

    # Refreshes all the widgets on screen
    def reloadWidgets(self, rowNum = 0, reloadEverything = False):
        self._pieChart.loadChart(self._selectedVersion)

        if (reloadEverything):
            self._modTable.loadTable(self._selectedVersion)
        else:
            # self._modTable.reloadTableRow(rowNum)
            self._modTable.loadTable(self._selectedVersion) # required for tests to work properly
        
        if self._savefunc is not None:
            self._savefunc(updatedProfile=mod.ModProfile(self._modList, self._priorityList, self._selectedVersion))

    # Simulates the user typing a URL and clicking the add mod button. Used for testing
    def simulate_enterAndAddMod(self, modURL:str):
        self._addModTextField.setText("")
        QtTest.QTest.keyClicks(self._addModTextField, modURL)
        QtTest.QTest.mouseClick(self._addModBtn, QtCore.Qt.MouseButton.LeftButton)

    # Simulates the user selecting a mod loader and clikced the download ready mods button. Used for testing
    def simulate_downloadMod(self, modLoaderOption:int):
        self._modLoaderDropdown.clickDropdownOption(modLoaderOption)
        return self._downloadReadyMods(True)
    
    def simulate_export(self, customFileName:str=False):
        if customFileName:
            fileName = customFileName
        else:
            fileName = "tests/testProfile.json"

        self._exportProfile(fileName, printDebugMessage=False)
    
    # Getters
    def getModTable(self): return self._modTable
    
    def getPieChart(self): return self._pieChart

    def getModList(self): return self._modList

    def getPriorityList(self): return self._priorityList

    def getSelectedVersion(self): return self._selectedVersion

    def _createWidgets(self):
        # create complex widgets
        self._pieChart = widgets.PieChart(self, self._modList, self._selectedVersion)
        self._modTable = widgets.ModTable_Manager(self, self._modList, self._priorityList,
                                              self._selectedVersion, self.reloadWidgets, self._savefunc)

        # create add mod widget
        self._addModBtn = widgets.createButton(self, "Add Mod", QtCore.QRect(800, 910, 200, 70), self._addMod, objectName="addModBtn")
        self._addModTextField = widgets.createTextField(self, "Enter mod URL here", QtCore.QRect(0, 910, 800, 70), objectName="addModTextField")
        self._errorLabel = widgets.createLabel(self, "Could not add mod. Invalid URL?", QtCore.QRect(1020, 910, 300, 70), objectName="errorLabel")
        self._errorLabel.setVisible(False)

        # create selected version widget
        self._selectedVersionLabel = widgets.createLabel(self, "Selected Version:", QtCore.QRect(1505, 10, 120, 50), objectName="selectedVersionLabel")
        self._selectedVersionTextField = widgets.createTextField(self, "", QtCore.QRect(1630, 10, 120, 50), objectName="selectedVersionTextField")
        self._selectedVersionTextField.setText(self._selectedVersion)

        # create download widget
        self._downloadBtn = widgets.createButton(self, "Download Ready Mods", QtCore.QRect(1525, 910, 275, 70), self._downloadReadyMods, objectName="downloadBtn")
        self._modLoaderDropdown = widgets.ModLoaderDropdownBtn(self, 0, QtCore.QRect(1800, 910, 110, 70))

        # create utility buttons
        self._refreshBtn = widgets.createButton(self, "", QtCore.QRect(1755, 10, 50, 50), self._refresh, objectName="refreshBtn", useSpecialSymbolFont=True)
        self._exportBtn = widgets.createButton(self, "", QtCore.QRect(1810, 10, 50, 50), self._exportProfile, objectName="exportBtn", useSpecialSymbolFont=True)
        self._exportLabel = widgets.createLabel(self, "Exported Successfully!", QtCore.QRect(1758, 50, 200, 70), objectName="exportLabel")
        self._exportLabel.setVisible(False)
        self._backBtn = widgets.createButton(self, "", QtCore.QRect(1865, 10, 50, 50), self._closeView, objectName="backBtn", useSpecialSymbolFont=True)

    # Adds a mod to the profile. Triggered when the add mod button is clicked
    def _addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self._addModTextField.text()  # this gets the input from the text field

        newMod = mod.Mod(url = inputString, modPriority=self._priorityList[0], tablePosition=len(self._modList))
        if newMod.isValid():
            self._modList.append(newMod)
            if self._savefunc is not None:
                self._savefunc(updatedProfile=mod.ModProfile(self._modList, self._priorityList, self._selectedVersion))
            self.reloadWidgets(reloadEverything=True)
            self._errorLabel.setVisible(False)
        else:
            self._errorLabel.setVisible(True)

    # Refreshes the data for each mod by making API calls and reloading the widgets
    def _refresh(self):
        self._selectedVersion = self._selectedVersionTextField.text()

        # refresh API. Use a thread for each refresh
        threadList = []
        for curMod in self._modList:
            thread = threading.Thread(target=curMod.refreshMod)
            thread.start()

        for thread in threadList:
            thread.join()

        self.reloadWidgets()
        if self._savefunc is not None:
            self._savefunc(updatedProfile=mod.ModProfile(self._modList, self._priorityList, self._selectedVersion))

    # Downloads every mod that is marked as ready in the mod table
    def _downloadReadyMods(self, preventDownload = False):
        successful_downloads = []
        
        if preventDownload == False:
            # create a pop up box that asks the user if they want to proceed
            popup = QtWidgets.QMessageBox(self)
            popup.setWindowTitle("Download Warning")
            popup.setText(f"Mod Tracker is about to open up to {len(self._modList)} tabs in your web browser to download your mods. Do you want to continue?")
            popup.setIcon(QtWidgets.QMessageBox.Icon.Information)
            popup.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            popupAnswer = popup.exec()

            # if the user does want to continue, download each mod that's ready
            if popupAnswer == QtWidgets.QMessageBox.StandardButton.Yes:
                for mod in self._modList:
                    if self._selectedVersion in mod.getVersionList():
                        # downloadMod returns True if a mod was downloaded, and False if not. Remember these results by adding them to a list
                        successful_downloads.append(mod.downloadMod(self._modLoaderDropdown.getSelectedModLoader(), self._selectedVersion, preventDownload=preventDownload))
                    else:
                        # Remember that this mod was not successfully downloaded
                        successful_downloads.append(False)
        else:
            # download each mod that's ready
            for mod in self._modList:
                if self._selectedVersion in mod.getVersionList():
                    # downloadMod returns True if a mod was downloaded, and False if not. Remember these results by adding them to a list
                    successful_downloads.append(mod.downloadMod(self._modLoaderDropdown.getSelectedModLoader(), self._selectedVersion, preventDownload=preventDownload))
                else:
                    # Remember that this mod was not successfully downloaded
                    successful_downloads.append(False)

        # return list of results
        return successful_downloads
    
    # Has the user select a directory and enter a file name, and then exports the profile as a json file
    def _exportProfile(self, directPath:str=False, printDebugMessage=True):
        if directPath == False:
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a directory")

            if directory:
                fileName, dialogSubmitted = QtWidgets.QInputDialog.getText(None, "Enter file name", "File name:")
                if dialogSubmitted and fileName:
                    path = f"{directory}/{fileName}.json"
                else:
                    path = False
            else:
                path = False
        else:
            path = directPath
            fileName = "Test Profile"

        if path != False:
            profile = mod.ModProfile(self._modList, self._priorityList, self._selectedVersion, fileName)

            if printDebugMessage:
                print(f"Exporting profile data to {path}")
            with open(path, "w") as file:
                json.dump(profile.createDict(), file, indent=4)
            
            self._exportLabel.setVisible(True)

    # Closes the details window and returns to the profile select window
    def _closeView(self):
        if self._savefunc is not None:
            self._savefunc(updatedProfile=mod.ModProfile(self._modList, self._priorityList, self._selectedVersion))
        self._onBackBtnClick()


# The display that allows the user to view all their profiles, and select one to open
class ProfileSelectWindow(QtWidgets.QWidget):
    _profileList:list[mod.ModProfile]
    _priorityList:list[mod.ModPriority]
    _allowWriteToFile:bool

    _profileWidgets:list[QtWidgets.QPushButton] = [] # currently unused
    _addProfileWidget:QtWidgets.QPushButton
    _currentProfileIndex:int # the index of the profile that's currently being displayed in the details view

    _widgetSize = 400 # size of the profile widget (width and height)
    _widgetSpacing = 35 # spacing between profile widgets
    _widgetsPerRow = 4 # number of profile widgets per row
    _maxWidgets = 8 # maximum number of profile widgets
    _numWidgets = 0 # current number of profile widgets
    _rowPadding = 30 # padding between the first row of profile widgets and the top of the window

    _titleFontSize = 24  # size of the profile widget's name text
    _subtitleFontSize = 20  # size of the rest of the text on a profile widget
    _plusSignFontSize = 32  # size of the plus sign on the add profile widget

    def __init__(self, onProfileClick, profileList:list[mod.ModProfile] = [], priorityList:list[mod.ModPriority] = [], allowWriteToFile = True):
        super().__init__()  # Initialize QWidget
        self._onProfileClick = onProfileClick
        self._profileList = profileList
        self._priorityList = priorityList
        self._allowWriteToFile = allowWriteToFile

        self._updatePriorityLists()

        self._addProfileWidget = None

        # Create a grid layout for managing widgets
        self._layout = QtWidgets.QGridLayout()
        self._layout.setSpacing(self._widgetSpacing)
        self.setLayout(self._layout)

        self._createWidgetRows()

    def addProfile(self, newProfile:mod.ModProfile, profileName:str = None, saveToFile = True):
        if not profileName or profileName == "":
            dialog = QtWidgets.QInputDialog(self)
            inputStr, okPressed = dialog.getText(self, "Create new mod profile", "New mod profile name:")
            if okPressed and len(inputStr) > 0:
                newProfile.name = inputStr
                self._profileList.append(newProfile)
                self._createProfileWidget()
                self.sortModLists()
                self.saveJson()
        else:
            newProfile.name = profileName
            self._profileList.append(newProfile)
            self._updatePriorityLists()
            self._createProfileWidget()
            self.sortModLists()

        if saveToFile:
            self.saveJson()

    # Write the details of each profile to a json file
    def saveJson(self, filename="mods.json", updatedProfile:mod.ModProfile = None):
        # Update the profile that was just changed in the details view. Don't change the name
        if updatedProfile is not None:
            currentProfile = self._profileList[self._currentProfileIndex]
            currentProfile.modList = updatedProfile.modList
            currentProfile.priorityList = updatedProfile.priorityList
            currentProfile.selectedVersion = updatedProfile.selectedVersion

        if self._allowWriteToFile:
            appdata = os.getenv('APPDATA')
            directory = os.path.join(appdata, 'ModTracker')
            os.makedirs(directory, exist_ok=True)
            json_path = os.path.join(directory, filename)

            print(f"Saving data to {json_path}")
            with open(json_path, "w") as file:
                json.dump([profile.createDict() for profile in self._profileList], file, indent=4)

        # reload UI
        self._createWidgetRows()

    def deleteProfile(self, numProfile):
        profileWidget = self._profileWidgets[numProfile]
        self._profileWidgets.remove(profileWidget)
        self._layout.removeWidget(profileWidget)
        profileWidget.deleteLater()

        self._profileList.remove(self._profileList[numProfile])

        self._deleteWidgetRows()
        self._updatePriorityLists()
        self.sortModLists()
        self.saveJson()

    def sortModLists(self):
        for profile in self._profileList:
            profile.modList.sort()

    # Simulates importing a mod. Used for testing. RequireValidMod will allow mods without a valid URL to be tested.
    def simulate_import(self, directPath:str=False, requireValidModURL=True):
        if directPath:
            fileName = directPath
        else:
            fileName = "tests/testProfile"

        self._importFromJSON(directPath=fileName, profileName="Test Profile", requireValidModURL=requireValidModURL)

    # Getters
    def getProfileList(self): return self._profileList

    def getPriorityList(self): return self._priorityList

    def _updatePriorityLists(self):
        for profile in self._profileList:
            for mod in profile.modList:
                if mod.priority not in self._priorityList:
                    self._priorityList.append(mod.priority)
        
        for profile in self._profileList:
            profile.priorityList = self._priorityList

    # Creates all profile widgets. Creates an add profile widget if there are no profiles
    def _createWidgetRows(self):
        self._profileWidgets = []
        self._numWidgets = 0

        if (len(self._profileList) == 0):
            self._createAddProfileWidget()
        else:
            for profile in self._profileList:
                self._createProfileWidget()

    def _deleteWidgetRows(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self._numWidgets = 0

    # Create a new widget that will display basic information about a profile and when clicked, will open the details view for that profile
    def _createProfileWidget(self):
        if (self._numWidgets >= self._maxWidgets):
            return

        # Create a profile widget, which is a button that will be used to open the profile
        profileWidget = QtWidgets.QPushButton()
        profileWidget.setFixedSize(self._widgetSize, self._widgetSize)

        # Connect _openDetailsView() to the underlying button
        profileWidget.clicked.connect(lambda checked, id = self._numWidgets: self._openDetailsView(id))

        # Profile name label
        widgets.createLabel(profileWidget, self._profileList[self._numWidgets].name, QtCore.QRect(10, 25, self._widgetSize - 20, 150),
                            fontSize=self._titleFontSize, bold=True, alignment=QtCore.Qt.AlignmentFlag.AlignCenter, wordWrap=True)

        # Mod count label
        widgets.createLabel(profileWidget, f"{len(self._profileList[self._numWidgets].modList)} mods", QtCore.QRect(10, 215, self._widgetSize - 20, 30),
                            fontSize=self._subtitleFontSize, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Readiness label
        widgets.createLabel(profileWidget, f"{self._profileList[self._numWidgets].getPercentReady():.2f}% ready\nfor {self._profileList[self._numWidgets].selectedVersion}",
                            QtCore.QRect(10, 280, self._widgetSize - 20, 60), fontSize=self._subtitleFontSize, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Delete button
        widgets.createButton(profileWidget, "X", QtCore.QRect(self._widgetSize - 55, 5, 50, 50), lambda checked, id = self._numWidgets: self.deleteProfile(id))

        # Add to list of profile widgets
        self._profileWidgets.append(profileWidget)

        # Add the widget to the grid layout
        row = self._numWidgets // self._widgetsPerRow
        col = self._numWidgets % self._widgetsPerRow
        self._layout.addWidget(profileWidget, row, col)

        # Increment the widget count and create add profile widget
        self._numWidgets += 1

        self._createAddProfileWidget()

    # Creates an additional widget with a plus sign that when clicked, will create a new profile
    def _createAddProfileWidget(self):
        # delete previous profile widget
        if (self._addProfileWidget is not None):
            self._addProfileWidget.deleteLater()

        if (self._numWidgets >= self._maxWidgets or self._numWidgets < len(self._profileList)):
            return

        self._addProfileWidget = QtWidgets.QPushButton(text="+")
        self._addProfileWidget.setFixedSize(self._widgetSize, self._widgetSize)
        self._addProfileWidget.clicked.connect(self._chooseCreateProfileOption)

        # Set font
        font = QtGui.QFont()
        font.setPointSize(self._titleFontSize)
        font.setBold(True)
        self._addProfileWidget.setFont(font)

        # Add the widget to the grid layout
        row = self._numWidgets // self._widgetsPerRow
        col = self._numWidgets % self._widgetsPerRow
        self._layout.addWidget(self._addProfileWidget, row, col)

    # Open details view for a given profile
    def _openDetailsView(self, profileNum: int):
        self._currentProfileIndex = profileNum
        profile = self._profileList[profileNum]
        self._onProfileClick(profile)

    # Opens dialog to enter a profile name and choose an import option. Runs when the import button is pressed.
    def _chooseCreateProfileOption(self):
        dialog = MultipleChoiceWindow(
            ["Create new profile", "Import from JSON file", "Import from mods folder", "Cancel"],
            windowTitle="Create a profile",
            showTextInput=True,
            textInput_labelText="Profile Name:",
            textInput_placeholderText="Enter profile name here"
        )

        choice = dialog.exec()
        profileName = dialog.getInputFieldText()

        match choice:
            case 1:
                self.addProfile(mod.ModProfile(), profileName=profileName)
            case 2:
                self._importFromJSON(profileName=profileName)
            case 3:
                self._importFromFolder(profileName=profileName)

    def _importFromJSON(self, directPath:str=False, profileName = None, requireValidModURL = True):
        if directPath:
            path = directPath
        else:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select a json file", filter="JSON Files (*.json)")

        if path:
            profile = load.createProfile(path, requireValidModURL=requireValidModURL)

            if profile:
                self.addProfile(profile, profileName)

    def _importFromFolder(self, profileName = None, directory:str = None, showPopups = True):
        if not directory:
            modsFolder = os.path.join(os.environ["APPDATA"], ".minecraft", "mods")
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a directory", modsFolder)

            if not directory:
                return
            
        if showPopups:
            disclaimerDialog = QtWidgets.QMessageBox(None)
            disclaimerDialog.setWindowTitle("Import Information")
            disclaimerDialog.setText(
                "Mod Tracker will search Modrinth and CurseForge for mods matching the ones in the folder you have selected. "
                "However, the correct mod cannot always be found.\n\n"
                "Please check that Mod Tracker added the correct mods when the import is complete."
            )
            disclaimerDialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)

            disclaimerAcknowledged = disclaimerDialog.exec()
            if disclaimerAcknowledged != QtWidgets.QMessageBox.StandardButton.Ok:
                return

            self._loadingWindow = LoadingWindow()
            self._loadingWindow.show()
        
        newProfile = readJarFile.createProfileFromFolder(directory)

        if showPopups:
            self._loadingWindow.close()

        self.addProfile(newProfile, profileName)
