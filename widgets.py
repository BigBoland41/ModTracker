from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import mod, os, sys

_btnFontSize = 18
_specialSymbolFontSize = 16
_labelFontSize = 12

_fontelloPath:str


# Represents the first cell of a row in the mod table.
# Displays the mod's name and "open link in browser" icon, as well as holds the mod object.
class ModTable_NameCell(QtWidgets.QWidget):
    modObj:mod.Mod
    _textFontSize = 14
    _iconFontSize = 12

    def __init__(self, modObj:mod.Mod):
        self.modObj = modObj
        super().__init__()

        # Create "open link in browser" icon
        icon_label = createLabel(labelText="  ", fontSize=self._iconFontSize, useSpecialSymbolFont=True)
        icon_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        icon_label.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        # Make icon clickable (open URL)
        def open_url():
            url = self.modObj.getURL()
            if url:
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        icon_label.mousePressEvent = lambda event: open_url()

        # Name label to show mod name
        name_label = createLabel(labelText=self.modObj.getName(),fontSize=self._textFontSize)

        # Layout for both labels
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(2)  # Reduce spacing

        icon_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        name_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        hbox.addWidget(icon_label)
        hbox.addWidget(name_label)
        hbox.addStretch(1)  # Push content to the left

        self.setLayout(hbox)


# Displays the data held in ModTable_Manager and handles user interaction with the mod table.
class ModTable_Widget(QtWidgets.QTableWidget):
    _parentWidget:QtWidgets.QWidget
    _dropdownBtnList:list['PriorityDropdownManager'] = []
     
    _tableLength = 1000
    _tableHeight = 900
    _headingHeight = 40
    _numColumns = 4
    _columnNames = ["Mod Name", "Latest Version", "Ready/Priority", ""]
    _columnWidths = [500, 160, 250, 10]
    _rowHeight = 50

    # The font size for everything in the table
    _fontSize = 14

    def __init__(self, parent, onRemoveRow=None, onDropCallback=None, reloadFunc=None):
        super().__init__(parent)
        self._parentWidget = parent
        self._onRemoveRow = onRemoveRow
        self._onDropCallback = onDropCallback
        self._reloadFunc = reloadFunc

        self._last_hovered_row = -1
        self._source_row = -1  # The row index where the current drag originated. Set on mouse press.
        self._destination_row = -1  # The row index where the current drag will end. Set on drop.

        self.setGeometry(QtCore.QRect(0, 0, self._tableLength, self._tableHeight))
        self.setObjectName("tableWidget")
        self.setColumnCount(self._numColumns)

        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

    def loadTable(self, rowCount:int):
        # set the row count to make the amount of mods in the list
        self.setRowCount(rowCount)

        # prepare font
        font = QtGui.QFont()
        font.setPointSize(self._fontSize)
        self.setFont(font)

        # configure headings
        for col in range(self._numColumns):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(18)
            item.setFont(font)
            item.setText(self._columnNames[col])
            self.setHorizontalHeaderItem(col, item)
            self.setColumnWidth(col, self._columnWidths[col])

    def setAllRows(self, modList, selectedVersion:str, priorityList):
        for rowNum, mod in enumerate(modList):
            self.setRow(rowNum, mod, selectedVersion, priorityList)

    def setRow(self, rowNum:int, mod:mod.Mod, selectedVersion:str, priorityList):
        self.setRowHeight(rowNum, self._rowHeight)
        
        self._setRowName(rowNum, mod)
        self._setRowVersion(rowNum, mod)
        self._createDropdownBtn(rowNum, mod, selectedVersion, priorityList)
        self._createDeleteBtn(rowNum)

    def removeTableRow(self, rowNum:int):
        self.removeRow(rowNum)
        self._dropdownBtnList.pop(rowNum)
        
        if callable(self._onRemoveRow):
            self._onRemoveRow(rowNum)

    def getRowDropdownBtn(self, rowNum:int):
        if 0 <= rowNum < len(self._dropdownBtnList):
            return self._dropdownBtnList[rowNum]
        
    def clearDropdownList(self):
        self._dropdownBtnList.clear()

    def _createBaseItem(self):
        item = QtWidgets.QTableWidgetItem()

        # create font object and set its font size
        font = QtGui.QFont()
        font.setPointSize(self._fontSize)
        item.setFont(font)

        return item

    def _setRowName(self, rowNum:int, mod:mod.Mod):
        item = self._createBaseItem()

        # if we're running from a file that isn't main.py, show testing text.
        if sys.argv[0][-7:] != "main.py":
            item.setText(mod.getName())

        nameItem = ModTable_NameCell(mod)
        self.setCellWidget(rowNum, 0, nameItem)

        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.setItem(rowNum, 0, item)

    def _setRowVersion(self, rowNum:int, mod:mod.Mod):
        item = self._createBaseItem()

        item.setText(mod.getCurrentVersion())

        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.setItem(rowNum, 1, item)

    # creates a button that opens the priority dropdown menu
    def _createDropdownBtn(self, rowNum:int, mod:mod.Mod, selectedVersion:str, priorityList):
        isReady = selectedVersion in mod.getVersionList()
        dropdownBtn = PriorityDropdownManager(self._parentWidget, mod, priorityList, self._reloadFunc, rowNum, isReady, self._fontSize)
        self.setCellWidget(rowNum, 2, dropdownBtn.getButtonWidget())
        self._dropdownBtnList.append(dropdownBtn)

    def _createDeleteBtn(self, rowNum:int):
        deleteBtn = QtWidgets.QPushButton("X")
        deleteBtn.clicked.connect(lambda : self.removeTableRow(rowNum))
        self.setCellWidget(rowNum, 3, deleteBtn)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        try:
            pos = event.position().toPoint()
        except Exception:
            pos = event.pos()

        idx = self.indexAt(pos)
        self._source_row = idx.row() if idx.isValid() else -1

        super().mousePressEvent(event)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        try:
            pos = event.position().toPoint()
        except Exception:
            pos = event.pos()

        idx = self.indexAt(pos)
        self._destination_row = idx.row() if idx.isValid() else self.rowCount()
        # print(f"{self._source_row} -> {self._destination_row}")

        super().dropEvent(event)

        if callable(self._onDropCallback):
            try:
                self._onDropCallback()
            except Exception:
                pass

    def getDestinationRow(self): return self._destination_row

    def getSourceRow(self): return self._source_row


# Manages the data displayed in the mod table and tells ModTable_Widget what to display.
class ModTable_Manager():
    # The PyQt6 table widget we are managing
    _tableWidget:ModTable_Widget
    # The parent object this widget is attached to
    _parentWidget:QtWidgets.QWidget

    # The list of mod to display
    _modList:list[mod.Mod]
    # The list of priority levels
    _priorityList:list[mod.Priority]
    # The selected version for this profile
    _selectedVersion:str
    
    def __init__(self, parent:QtWidgets.QWidget, modList:list[mod.Mod], priorityList:list[mod.Priority], selectedVersion:str, reloadFunc, saveFunc):
        self._parentWidget = parent
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self._reloadFunc = reloadFunc
        self._saveFunc = saveFunc
        self._tableWidget = ModTable_Widget(self._parentWidget, self._onRowRemoved, self._updateRowOrder, self._reloadFunc)
        self.loadTable()

    def loadNewData(self, modList, priorityList, selectedVersion):
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self.loadTable()

    def createDict(self):
        dict = {}
        for mod in self._modList:
            dict.append(mod.createDict())
        return dict

    def loadTable(self, selectedVersion:str = ""):
        if selectedVersion != "":
            self._selectedVersion = selectedVersion

        self._tableWidget.loadTable(len(self._modList))
        self._tableWidget.setAllRows(self._modList, self._selectedVersion, self._priorityList)

    def reloadTableRow(self, rowNum:int):
        self._tableWidget.setRow(rowNum, self._modList[rowNum], self._selectedVersion, self._priorityList)

    # Getters
    def getModList(self): return self._modList

    def getTableWidget(self): return self._tableWidget

    def getRowNameText(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            return self._tableWidget.item(rowNum, 0).text()
    
    def getRowVersionText(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            return self._tableWidget.item(rowNum, 1).text()

    def getRowDropdownBtnText(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            return self._tableWidget.cellWidget(rowNum, 2).text()

    def getRowDropdownBtn(self, rowNum:int):
        return self._tableWidget.getRowDropdownBtn(rowNum)
        
    def getRowDeleteBtn(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            return self._tableWidget.cellWidget(rowNum, 3)
    
    def getNumRows(self): return self._tableWidget.rowCount()
    
    def clickRowDeleteBtn(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            self._tableWidget.cellWidget(rowNum, 3).click()

    # removes a mod from the table and mod list
    def _onRowRemoved(self, rowNum:int):
        mod = self._modList[rowNum]
        self._modList.remove(mod)

        self._reloadFunc()
        if callable(self._saveFunc):
            self._saveFunc()

    # Updates the tablePosition of each mod to match their row's position in _tableWidget.
    # Called after a drag and drop operation.
    def _updateRowOrder(self):
        sourceRow = self._tableWidget.getSourceRow()
        destinationRow = self._tableWidget.getDestinationRow()
        sourceRowItem = self._tableWidget.item(self._tableWidget.getSourceRow(), 0)

        if not sourceRowItem:
            self._swapRows(sourceRow, destinationRow)
        else:
            self._reorderRows()

        # apply updates
        self._modList.sort()
        self.loadTable()
        self._reloadFunc()

    def _reorderRows(self):
        # for each row (if row is valid), make the corresponding mod's tablePosition match the row's position
        for rowNum in range(self._tableWidget.rowCount()):
            nameWidget = self._tableWidget.cellWidget(rowNum, 0)
            if nameWidget:
                nameWidget.modObj.tablePosition = rowNum
            else:  # an invalid row was found. Stop.
                break

    def _swapRows(self, sourceRow:int, destinationRow:int):
        sourceMod = None
        destinationMod = None

        for modObj in self._modList:
            if modObj.tablePosition == sourceRow:
                sourceMod = modObj
            if modObj.tablePosition == destinationRow:
                destinationMod = modObj

        # destinationMod = self._getModFromRow(destinationRow)
        
        if sourceMod and destinationMod:
            sourceMod.tablePosition = destinationRow
            destinationMod.tablePosition = sourceRow
        else:
            print(f"Failed to swap rows {sourceRow} and {destinationRow}, whose mods were {sourceMod} and {destinationMod}")


# Button that when clicked, displays a dropdown menu.
class DropdownBtn():
    _parentWidget:QtWidgets.QWidget
    _menuOptions:list[str]
    _buttonRect:QtCore.QRect
    _selectedOption:int
    _fontSize:int
    _includeCarrot:bool
    _customButtonText:str

    _buttonWidget:QtWidgets.QPushButton
    _menuWidget:QtWidgets.QMenu


    def __init__(self, parentWidget:QtWidgets.QWidget, menuOptions:list[str], onOptionClick = None,
                 buttonRect:QtCore.QRect = None, selectedOption = 0, buttonFontSize = 14,
                 includeCarrot = True, customButtonText:str = None):
        self._parentWidget = parentWidget
        self._menuOptions = menuOptions
        self._onOptionClick = onOptionClick
        self._buttonRect = buttonRect
        self._selectedOption = selectedOption
        self._fontSize = buttonFontSize
        self._includeCarrot = includeCarrot
        self._customButtonText = customButtonText

        self._createButtonWidget()
        self._createMenuWidget()

    def clickDropdownOption(self, index):
        if self._menuOptions and 0 <= index < len(self._menuWidget.actions()):
            self._clickOption(index)

    def setStyleSheet(self, backgroundColor = "gray", textColor = "black", fontSize:int = None):
        if not fontSize:
            fontSize = self._fontSize

        self._buttonWidget.setStyleSheet(f"background-color: {backgroundColor};"
                                          + f"color: {textColor};"
                                          + f"font-size: {fontSize}px;")
        
    def setCustomButtonText(self, customButtonText:str):
        self._customButtonText = customButtonText
        self._buttonWidget.setText(self._customButtonText)

    def getSelectedOption(self):
        return self._menuOptions[self._selectedOption]
    
    def getOptions(self):
        return self._menuOptions

    def getButtonWidget(self):
        return self._buttonWidget
    
    def getMenuWidget(self):
        return self._menuWidget

    def _createButtonWidget(self):
        # create font for button
        buttonFont = QtGui.QFont()
        buttonFont.setPointSize(self._fontSize)
        
        # create button
        self._buttonWidget = QtWidgets.QPushButton(parent=self._parentWidget)
        if self._buttonRect:
            self._buttonWidget.setGeometry(self._buttonRect)
        self._buttonWidget.setFont(buttonFont)
        self._updateButtonText()

        self._buttonWidget.clicked.connect(
            lambda : self._menuWidget.exec(
                self._buttonWidget.mapToGlobal(self._buttonWidget.rect().bottomLeft())))
        
    def _createMenuWidget(self):
        self._menuWidget = QtWidgets.QMenu(self._parentWidget)

        for i in range(len(self._menuOptions)):
            self._menuWidget.addAction(self._menuOptions[i], lambda index=i : self._clickOption(index))

    def _clickOption(self, index):
        self._selectedOption = index
        self._updateButtonText()
        
        if self._onOptionClick and callable(self._onOptionClick):
            self._onOptionClick(index)

    def _updateButtonText(self):
        if self._customButtonText:
            self._buttonWidget.setText(self._customButtonText)
        elif self._includeCarrot:
            self._buttonWidget.setText(self._menuOptions[self._selectedOption] + " ▾")
        else:
            self._buttonWidget.setText(self._menuOptions[self._selectedOption])


# Manages the dropdown menu that appears in the third column of the table which allows
# the user to select a priorty level, or create a new priority level.
class PriorityDropdownManager():
    _parentWidget:QtWidgets.QWidget
    _buttonWidget:QtWidgets.QPushButton
    _menuWidget:QtWidgets.QMenu
    _mod:mod.Mod
    _priorityList:list[mod.Priority]
    _rowNum:int
    _fontSize:int

    def __init__(self, parentWidget:QtWidgets.QWidget, mod:mod.Mod, priorityList:list[mod.Priority],
                 refreshFunc, rowNum:int, isReady:bool, fontSize:int):
        # set attributes
        self._parentWidget = parentWidget
        self._mod = mod
        self._priorityList = priorityList
        self._refreshFunc = refreshFunc
        self._rowNum = rowNum
        self._fontSize = fontSize

        # run setup functions
        self._createDropdownWidget()
        self._customizeAppearance(isReady)

    def clickDropdownOption(self, index, priorityName:str = None, priorityColor:QtGui.QColor = None):
        menuWidget = self._dropdownWidget.getMenuWidget()
        listLength = len(menuWidget.actions()) - 1

        if 0 <= index < listLength:
            self._changeModPriority(index)
        elif index == listLength:
            if priorityName:
                self._addModPriority(priorityName, priorityColor)
            else:
                self._showPrompts()

    def getDropdownWidget(self):
        return self._dropdownWidget

    def getButtonWidget(self):
        return self._dropdownWidget.getButtonWidget()
    
    def getMenuWidget(self):
        return self._dropdownWidget.getMenuWidget()

    def _createDropdownWidget(self):
        dropdownOptions = []
        for priorityLevel in self._priorityList:
            dropdownOptions.append(priorityLevel.name)
        dropdownOptions.append("Add Priority Level")

        try:
            curPriorityIndex = self._priorityList.index(self._mod.priority)
        except ValueError:
            curPriorityIndex = 0

        self._dropdownWidget = DropdownBtn(self._parentWidget, dropdownOptions, self.clickDropdownOption, selectedOption=curPriorityIndex, includeCarrot=False)

    def _customizeAppearance(self, isReady:bool):
        if (isReady):
            backgroundColor = QtGui.QColor(0, 255, 0)
            self._dropdownWidget.setCustomButtonText("Ready")
        else:
            backgroundColor = self._mod.priority.color
        
        self._dropdownWidget.setStyleSheet(backgroundColor.name())

    def _changeModPriority(self, index, refreshEverything = False):
        self._mod.priority = self._priorityList[index]

        if self._refreshFunc and callable(self._refreshFunc):
            self._refreshFunc(self._rowNum, refreshEverything)

    def _showPrompts(self):
        inputStr, okPressed = QtWidgets.QInputDialog.getText(self._parentWidget, "Create new priority level", "Priority name:")
        
        if okPressed:
            selectedColor = QtWidgets.QColorDialog.getColor()
            if (selectedColor.isValid()):
                self._addModPriority(inputStr, selectedColor)

    def _addModPriority(self, modName:str, color:QtGui.QColor):
        if not modName:
            modName = "New Priority Level"

        self._priorityList.append(mod.Priority(modName, color=color))
        self._changeModPriority(len(self._priorityList) - 1, True)  # select new priority level


# This is the pie chart that displays how many of the mods in this profile are ready,
# and then breaks down the rest by priority level.
class PieChart():
    _parentWidget: QtWidgets.QWidget
    _modList: list[mod.Mod]
    _selectedVersion: str

    _chartView: QtCharts.QChartView
    _series: QtCharts.QPieSeries
    _readySlice = mod.Priority("Ready", 0, 255, 0)
    _sliceSizes = {_readySlice: 0}

    _titleFontSize = 24
    _labelFontSize = 14

    def __init__(self, parent:QtWidgets.QWidget, modList:list[mod.Mod], selectedVersion:str):
        # Assign variables
        self._parentWidget = parent
        self._modList = modList
        self._selectedVersion = selectedVersion

        self._series = QtCharts.QPieSeries()
        self._chartView = QtCharts.QChartView(parent=self._parentWidget)
        self._chartView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._chartView.setGeometry(QtCore.QRect(1000, 50, 900, 900))

        self.loadChart()

    def getSliceSizes(self): return self._sliceSizes

    def loadNewData(self, modList, priorityList, selectedVersion):
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self.loadChart()

    def loadChart(self, selectedVersion:str = ""):
        if selectedVersion != "":
            self._selectedVersion = selectedVersion

        # Calculate the size of each slice
        self._calculateSliceSizes()

        # Create chart and add pie slices to it
        chart = QtCharts.QChart()
        self._createSeries()
        chart.addSeries(self._series)

        # Create title text
        title_font = QtGui.QFont()
        title_font.setPointSize(self._titleFontSize)
        chart.setTitle('Mod Priority Chart')
        chart.setTitleFont(title_font)
        if (isDarkTheme()):
            chart.setTitleBrush(QtGui.QBrush(QtGui.QColor("white")))

        # Hide legend and set background color
        chart.legend().hide()
        chart.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

        # Update the existing chart view
        self._chartView.setChart(chart)

    def _calculateSliceSizes(self):
        self._sliceSizes = {self._readySlice: 0}
        for mod in self._modList:
            if self._selectedVersion in mod.getVersionList():
                self._sliceSizes[self._readySlice] += 1
            else:
                if mod.priority in self._sliceSizes:
                    self._sliceSizes[mod.priority] += 1
                else:
                    self._sliceSizes[mod.priority] = 1

    def _createSeries(self):
        label_font = QtGui.QFont()
        label_font.setPointSize(self._labelFontSize)
        darkTheme = isDarkTheme()

        # Create and populate chart series
        self._series.__init__()
        self._series.clear()

        i = 0
        for priority, count in self._sliceSizes.items():
            self._series.append(priority.name, count)
            slice = self._series.slices()[i]

            if priority == self._readySlice:
                slice.setExploded()

            slice.setColor(priority.color)
            slice.setBorderColor(priority.color)

            slice.setLabelVisible()
            slice.setLabelFont(label_font)
            if darkTheme:
                slice.setLabelColor(QtGui.QColor("white"))
            i += 1


# Displays basic information about a profile that when clicked, will open the details view for that profile.
# Can optionally be set to only display a + sign instead of default labels.
class ProfileButton(QtWidgets.QPushButton):
    profile:mod.Profile
    widgetNum:int

    _widgetSize = 400
    _titleFontSize = 24
    _subtitleFontSize = 20
    _plusSignFontSize = 32

    _nameLabel:QtWidgets.QLabel
    _modCountLabel:QtWidgets.QLabel
    _percentReadyLabel:QtWidgets.QLabel
    _deleteBtn:QtWidgets.QPushButton

    def __init__(self, onClick, profile:mod.Profile = None, onDelete = None, widgetNum:int = None, onlyDisplayPlusSign = False):
        self.profile = profile
        self.widgetNum = widgetNum
        self._onClick = onClick
        self._onDelete = onDelete
        super().__init__()

        self.setFixedSize(self._widgetSize, self._widgetSize)
        self.clicked.connect(self._clicked)

        if onlyDisplayPlusSign:
            self.setText("+")
            font = QtGui.QFont()
            font.setPointSize(self._titleFontSize)
            font.setBold(True)
            self.setFont(font)
        else:
            self._nameLabel = createLabel(
                self,
                self.profile.name,
                QtCore.QRect(10, 25, self._widgetSize - 20, 150),
                fontSize=self._titleFontSize,
                bold=True,
                alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
                wordWrap=True
            )

            self._modCountLabel = createLabel(
                self,
                f"{len(self.profile.modList)} mods",
                QtCore.QRect(10, 215, self._widgetSize - 20, 30),
                fontSize=self._subtitleFontSize,
                alignment=QtCore.Qt.AlignmentFlag.AlignCenter
            )

            self._percentReadyLabel = createLabel(
                self,
                f"{self.profile.getPercentReady():.2f}% ready\nfor {self.profile.selectedVersion}",
                QtCore.QRect(10, 280, self._widgetSize - 20, 60),
                fontSize=self._subtitleFontSize,
                alignment=QtCore.Qt.AlignmentFlag.AlignCenter
            )
            
            if self._onDelete and callable(self._onDelete):
                self._deleteBtn = createButton(self, "X", QtCore.QRect(self._widgetSize - 55, 5, 50, 50), self._deleteBtnClicked)

    def _clicked(self):
        if self._onClick and callable(self._onClick):
            if self.widgetNum is None:
                self._onClick()
            else:
                self._onClick(self.widgetNum)

    def _deleteBtnClicked(self):
        if self._onDelete and callable(self._onDelete):
            self._onDelete(self.widgetNum)


# Grid layout embedded in the profile select window that contains all the profile buttons.
class ProfileSelectLayout(QtWidgets.QGridLayout):
    _profileWidgets:list[QtWidgets.QPushButton] = [] # currently unused
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

    def __init__(self, parent, onProfileClick, onCreateProfile, onProfileDelete, getProfileList):
        super().__init__(parent)
        self._onProfileClick = onProfileClick
        self._onCreateProfile = onCreateProfile
        self._onProfileDelete = onProfileDelete
        self._getProfileList = getProfileList

        self._addProfileWidget = None

        self.setSpacing(self._widgetSpacing)

    # Creates all profile widgets. Creates an add profile widget if there are no profiles
    def createWidgetRows(self):
        profileList = self._getProfileList()
            
        self._profileWidgets = []
        self._numWidgets = 0

        if (len(profileList) == 0):
            self._createAddProfileWidget()
        else:
            for profile in profileList:
                self.createProfileWidget(profile)

    # Create a new widget that will display basic information about a profile and when clicked, will open the details view for that profile
    def createProfileWidget(self, profile:mod.Profile):
        if (self._numWidgets >= self._maxWidgets):
            return

        # Create a profile widget, which is a button that will be used to open the profile
        profileWidget = ProfileButton(self._onProfileClick, profile=profile, onDelete=self._deleteProfile, widgetNum=self._numWidgets)

        # Add to list of profile widgets
        self._profileWidgets.append(profileWidget)
        self._insertWidget(profileWidget)
        self._numWidgets += 1

        self._createAddProfileWidget()

    def _deleteWidgetRows(self):
        while self.count():
            item = self.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self._numWidgets = 0
    
    def _deleteProfile(self, numProfile):
        profileWidget = self._profileWidgets[numProfile]
        self._profileWidgets.remove(profileWidget)
        self.removeWidget(profileWidget)
        profileWidget.deleteLater()

        self._onProfileDelete(numProfile)

        self._deleteWidgetRows()
        self.createWidgetRows()

    # Creates an additional widget with a plus sign that when clicked, will create a new profile
    def _createAddProfileWidget(self):
        # delete previous profile widget
        if self._addProfileWidget:
            self._addProfileWidget.deleteLater()

        if (self._numWidgets >= self._maxWidgets):
            return

        self._addProfileWidget = ProfileButton(self._onCreateProfile, onlyDisplayPlusSign=True)
        self._insertWidget(self._addProfileWidget)

    def _insertWidget(self, profileButton:ProfileButton):
        row = self._numWidgets // self._widgetsPerRow
        col = self._numWidgets % self._widgetsPerRow
        self.addWidget(profileButton, row, col)

# ------------------------------
# HELPER FUNCTIONS FUNCTIONS
# ------------------------------

# Automatically runs when widgets is imported in another file.
def setFontelloPath():
    global _fontelloPath
    _fontelloPath = os.path.join(os.path.dirname(__file__), "fonts", "fontello.ttf")
    # print("Fontello path: " + _fontelloPath)

def _createLabelFont(fontSize:int = 0, bold = False, useSpecialSymbolFont = False):
    font = QtGui.QFont()
    
    if useSpecialSymbolFont:
        # Load custom font for special symbol
        font.setPointSize(_specialSymbolFontSize)
        global _fontelloPath
        font_path = _fontelloPath
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                font.setFamily(font_families[0])
    else:
        font.setPointSize(_labelFontSize)

    if fontSize > 0:
        font.setPointSize(fontSize)

    font.setBold(bold)

    return font

# Helper function for quickly making and customizing a QButton
def createButton(
        parent = None,
        btnText:str = "Button",
        geometry:QtCore.QRect = QtCore.QRect(),
        onClickFunc = None,
        objectName:str = None,
        fontSize:int = 0,
        bold = False,
        useSpecialSymbolFont = False,
        minimumWidth = 0,
        minimumHeight = 0
    ):
    if fontSize <= 0:
        fontSize = _btnFontSize
    
    font = _createLabelFont(fontSize, bold, useSpecialSymbolFont)

    button = QtWidgets.QPushButton(parent=parent)
    button.setFont(font)
    button.setText(btnText)
    button.setGeometry(geometry)

    if onClickFunc:
        button.clicked.connect(onClickFunc)

    if objectName:
        button.setObjectName(objectName)

    if minimumWidth > 0:
        button.setMinimumWidth(minimumWidth)

    if minimumHeight > 0:
        button.setMinimumHeight(minimumHeight)

    return button

# Helper function for quickly making and customizing a QLabel
def createLabel(
        parent = None,
        labelText:str = "Label",
        geometry:QtCore.QRect = QtCore.QRect(),
        objectName:str = None,
        fontSize:int = 0,
        bold = False,
        useSpecialSymbolFont = False,
        alignment:QtCore.Qt.AlignmentFlag = None, wordWrap = False
    ):
    font = _createLabelFont(fontSize, bold, useSpecialSymbolFont)

    label = QtWidgets.QLabel(parent=parent)
    label.setFont(font)
    label.setText(labelText)
    label.setGeometry(geometry)
    label.setWordWrap(wordWrap)

    if objectName != None:
        label.setObjectName(objectName)

    if alignment != None:
        label.setAlignment(alignment)

    return label

# Helper function for quickly making and customizing a QLineEdit
def createTextField(
        parent = None,
        placeholderText:str = "",
        geometry:QtCore.QRect = QtCore.QRect(),
        objectName:str = None,
        fontSize:int = 0,
        bold = False,
        useSpecialSymbolFont = False,
        alignment:QtCore.Qt.AlignmentFlag = None
    ):
    font = _createLabelFont(fontSize, bold, useSpecialSymbolFont)
    
    textField = QtWidgets.QLineEdit(parent=parent)
    textField.setFont(font)
    textField.setPlaceholderText(placeholderText)
    textField.setGeometry(geometry)

    if objectName != None:
        textField.setObjectName(objectName)

    if alignment != None:
        textField.setAlignment(alignment)

    return textField

def isDarkTheme():
    # Access Windows registry to check the theme setting
    settings = QtCore.QSettings("HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", QtCore.QSettings.Format.NativeFormat)

    # The registry key "AppsUseLightTheme" determines the theme
    light_theme = settings.value("AppsUseLightTheme", 1, type=int)
    return light_theme == 0  # 0 means dark theme, 1 means light theme


# Automatically set fontello path when widgets is imported.
setFontelloPath()