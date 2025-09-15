from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import mod, os

_btnFontSize = 18
_specialSymbolFontSize = 16
_labelFontSize = 12

_fontelloPath:str

# This is the table that displays information about all the mods in a profile, including the
# mod name, it's latest version, "ready" or it's priority level, and a button to remove the
# mod from the table. 
class ModTable():
    # How long the table is, in pixels
    _tableLength = 1000
    # How tall the table is, in pixels
    _tableHeight = 900
    # Height of the headings
    _headingHeight = 40

    # Number of columns in the table
    _numColumns = 4
    # Names of the columns
    _columnNames = ["Mod Name", "Latest Version", "Ready/Priority", ""]
    # Widths of the columns
    _columnWidths = [500, 160, 250, 10]
    # Height of the rows
    _rowHeight = 50

    # The font size for everything in the table
    _fontSize = 14

    # The PyQt6 table widget we are managing
    _tableWidget:QtWidgets.QTableWidget
    # The parent object this widget is attached to
    _parentWidget:QtWidgets.QWidget
    # List of dropdownBtn objects in the table
    _dropdownBtnList:list['PriorityDropdownBtn'] = []

    # The list of mod to display
    _modList:list[mod.Mod]
    # The list of priority levels
    _priorityList:list[mod.ModPriority]
    # The selected version for this profile
    _selectedVersion:str
    # Dictionary of mod names to mod objects
    _modNames = {}
    
    def __init__(self, parent:QtWidgets.QWidget, modList:list[mod.Mod], priorityList:list[mod.ModPriority],
                 selectedVersion:str, reloadFunc, saveFunc):
        self._parentWidget = parent
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self._reloadFunc = reloadFunc
        self._saveFunc = saveFunc
        self._createTable()
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

        # set the row count to make the amount of mods in the list
        self._tableWidget.setRowCount(len(self._modList))

        # prepare font
        font = QtGui.QFont()
        font.setPointSize(self._fontSize)
        self._tableWidget.setFont(font)

        # configure headings
        for col in range(self._numColumns):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(18)
            item.setFont(font)
            item.setText(self._columnNames[col])
            self._tableWidget.setHorizontalHeaderItem(col, item)
            self._tableWidget.setColumnWidth(col, self._columnWidths[col])

        # add rows to table and set row height
        for row in range(len(self._modList)):
            self._setTableRow(row, self._modList[row])
            self._tableWidget.setRowHeight(row, self._rowHeight)

    def reloadTableRow(self, rowNum:int):
        self._tableWidget.setRowCount(len(self._modList))
        self._setTableRow(rowNum, self._modList[rowNum])

    # Getters
    def getModList(self): return self._modList

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
        if 0 <= rowNum < len(self._dropdownBtnList):
            return self._dropdownBtnList[rowNum]
        
    def getRowDeleteBtn(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            return self._tableWidget.cellWidget(rowNum, 3)
    
    def getNumRows(self): return self._tableWidget.rowCount()
    
    def clickRowDeleteBtn(self, rowNum:int):
        if 0 <= rowNum < self._tableWidget.rowCount():
            self._tableWidget.cellWidget(rowNum, 3).click()

    # create and configure table
    def _createTable(self):
        self._tableWidget = QtWidgets.QTableWidget(self._parentWidget)
        self._tableWidget.setGeometry(QtCore.QRect(0, 0, self._tableLength, self._tableHeight))
        self._tableWidget.setObjectName("tableWidget")
        self._tableWidget.setColumnCount(self._numColumns)

        self._tableWidget.setDragDropOverwriteMode(False)
        self._tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self._tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self._tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # Add event filter to detect row reordering
        filter = DropEventFilter(self._tableWidget, self._reorderRows)
        self._tableWidget.installEventFilter(filter)
    
    # adds a row to the table with the proper mod information
    def _setTableRow(self, rowNum:int, mod:mod.Mod):
        for col in range(self._numColumns):
            # create table item
            item = QtWidgets.QTableWidgetItem()

            # create font object and set its font size
            font = QtGui.QFont()
            font.setPointSize(self._fontSize)
            item.setFont(font)

            # set the correct text/widget for each item in the row
            match col:
                case 0:
                    # This text won't appear, but is useful for testing
                    item.setText(mod.getName())

                    # Add mod name to dictionary. Useful for reordering the list.
                    self._modNames[mod.getName()] = mod

                    # Load custom font for special symbol
                    global _fontelloPath
                    font_path = _fontelloPath
                    font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
                        fontello_family = font_families[0] if font_families else "Arial"
                    else:
                        fontello_family = "Arial"

                    # Icon label with custom font
                    icon_label = QtWidgets.QLabel("  ")
                    icon_font = QtGui.QFont(fontello_family)
                    icon_font.setPointSize(self._fontSize - 2)
                    icon_label.setFont(icon_font)
                    icon_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
                    icon_label.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

                    # Make icon clickable (open URL)
                    def open_url():
                        url = mod.getURL()
                        if url:
                            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
                    icon_label.mousePressEvent = lambda event: open_url()

                    # Name label with Arial
                    name_label = QtWidgets.QLabel(mod.getName())
                    name_font = QtGui.QFont()
                    name_font.setPointSize(self._fontSize)
                    name_label.setFont(name_font)

                    # Layout for both labels
                    hbox = QtWidgets.QHBoxLayout()
                    hbox.setContentsMargins(0, 0, 0, 0)
                    hbox.setSpacing(2)  # Reduce spacing

                    icon_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
                    name_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

                    hbox.addWidget(icon_label)
                    hbox.addWidget(name_label)
                    hbox.addStretch(1)  # Optional: push content to the left

                    container = QtWidgets.QWidget()
                    container.setLayout(hbox)

                    self._tableWidget.setCellWidget(rowNum, 0, container)
                case 1:
                    item.setText(mod.getCurrentVersion())
                case 2:
                    # create dropdown button and put add it to this table item
                    self._createDropdownBtn(rowNum, mod)
                case 3:
                    deleteBtn = QtWidgets.QPushButton("X")
                    deleteBtn.clicked.connect(lambda : self._removeTableRow(mod))
                    self._tableWidget.setCellWidget(rowNum, 3, deleteBtn)

            # apply changes
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self._tableWidget.setItem(rowNum, col, item)

    # removes a mod from the table and mod list
    def _removeTableRow(self, mod:mod.Mod):
        self._tableWidget.removeRow(self._modList.index(mod))
        self._dropdownBtnList.pop(self._modList.index(mod))
        self._modList.remove(mod)
        self._reloadFunc()
        if callable(self._saveFunc):
            self._saveFunc()

    # creates all the buttons that reveal the priority dropdown menu
    def _createDropdownBtn(self, rowNum:int, mod:mod.Mod):
        dropdownBtn = PriorityDropdownBtn(self._parentWidget, mod, self._priorityList, self._reloadFunc,
                                  rowNum, self._selectedVersion in mod.getVersionList(), self._fontSize)
        self._tableWidget.setCellWidget(rowNum, 2, dropdownBtn.getButtonWidget())
        self._dropdownBtnList.append(dropdownBtn)

    def _reorderRows(self):
        for rowNum in range(self._tableWidget.rowCount()):
            rowNameItem = self._tableWidget.item(rowNum, 0)
            if rowNameItem:
                rowName = rowNameItem.text()
                modObj:mod.Mod = self._modNames[rowName]
                modObj.tablePosition = rowNum

        self._modList.sort()
        self.loadTable()


# Runs onTrigger() when a row in a table is drag and dropped to a new position
class DropEventFilter(QtCore.QObject):
    def __init__(self, parent, onTrigger):
        super().__init__(parent)
        self._dropFunc = onTrigger

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.ChildRemoved:
            self._dropFunc()

        return False

# This is the dropdown menu that appears in the third column of the table which allows
# the user to select a priorty level, or create a new priority level.
class PriorityDropdownBtn():
    _parentWidget:QtWidgets.QWidget
    _buttonWidget:QtWidgets.QPushButton
    _menuWidget:QtWidgets.QMenu
    _mod:mod.Mod
    _priorityList:list[mod.ModPriority]
    _rowNum:int
    _fontSize:int

    def __init__(self, parentWidget:QtWidgets.QWidget, mod:mod.Mod, priorityList:list[mod.ModPriority],
                 refreshFunc, rowNum:int, isReady:bool, fontSize:int):
        # set attributes
        self._parentWidget = parentWidget
        self._mod = mod
        self._priorityList = priorityList
        self._refreshFunc = refreshFunc
        self._rowNum = rowNum
        self._fontSize = fontSize

        # run setup functions
        self._createButtonWidget()
        self._createMenuWidget()
        self._customizeAppearance(isReady)

    def clickDropdownOption(self, index, priorityName = "New Priority Level", priorityColor = QtGui.QColor(255, 0, 0)):
        if 0 <= index < len(self._menuWidget.actions()) - 1:
            self._changeModPriority(index)
        elif index == len(self._menuWidget.actions()) - 1:
            self._addModPriority(priorityName, priorityColor)

    def getButtonWidget(self):
        return self._buttonWidget
    
    def getMenuWidget(self):
        return self._menuWidget

    def _createButtonWidget(self):
        # create button
        self._buttonWidget = QtWidgets.QPushButton(parent=self._parentWidget)

        # making the lambda its own function doesn't work for some reason
        self._buttonWidget.clicked.connect(
            lambda : self._menuWidget.exec(
                self._buttonWidget.mapToGlobal(self._buttonWidget.rect().bottomLeft())))
        
    def _createMenuWidget(self):
        # create dropdown menu
        self._menuWidget = QtWidgets.QMenu(self._parentWidget)

        # add priority levels to action list
        i = 0
        for priorityLevel in self._priorityList:
            self._menuWidget.addAction(priorityLevel.name,
                                        lambda index=i : self._changeModPriority(index))
            i += 1
        self._menuWidget.addAction("Add Priority Level", self._showColorPicker)

    def _customizeAppearance(self, isReady:bool):
        # If the mod version matches the selected version...
        if (isReady):
            # set color to green and set text to ready
            backgroundColor = QtGui.QColor(0, 255, 0)
            self._buttonWidget.setText("Ready")
        else:
            # set color to priority level color and set text to priority level name
            backgroundColor = self._mod.priority.color
            self._buttonWidget.setText(self._mod.priority.name)
        
        # set the background color the one chosen above
        self._buttonWidget.setStyleSheet(f"background-color: {backgroundColor.name()};"
                                          + f"color: black;"
                                          + f"font-size: {self._fontSize}px;")

    def _changeModPriority(self, index, refreshEverything = False):
        self._mod.priority = self._priorityList[index]
        if callable(self._refreshFunc):
            self._refreshFunc(self._rowNum, refreshEverything)

    def _showColorPicker(self):
        inputStr, okPressed = QtWidgets.QInputDialog.getText(
            self._parentWidget, "Create new priority level", "Priority name:"
        )
        
        if okPressed:
            selectedColor = QtWidgets.QColorDialog.getColor()
            if (selectedColor.isValid()):
                self._addModPriority(inputStr, selectedColor)

    def _addModPriority(self, modName:str, color:QtGui.QColor):
        self._priorityList.append(mod.ModPriority(modName, color=color))
        self._changeModPriority(len(self._priorityList) - 1, True)


# This is the pie chart that displays how many of the mods in this profile are ready,
# and then breaks down the rest by priority level.
class PieChart():
    _parentWidget: QtWidgets.QWidget
    _modList: list[mod.Mod]
    _selectedVersion: str

    _chartView: QtCharts.QChartView
    _series: QtCharts.QPieSeries
    _readySlice = mod.ModPriority("Ready", 0, 255, 0)
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


# This is the dropdown menu that appears next to the download button that allows
# the user to select which mod loader they prefer.
class ModLoaderDropdownBtn():
    _selectedModLoader:int

    _parentWidget:QtWidgets.QWidget
    _buttonRect:QtCore.QRect

    _buttonWidget:QtWidgets.QPushButton
    _menuWidget:QtWidgets.QMenu

    _modLoaderList = ["Forge", "Fabric", "NeoForge", "Quilt"]

    def __init__(self, parentWidget:QtWidgets.QWidget, selectedModLoader:int, buttonRect:QtCore.QRect):
        # set attributes
        self._parentWidget = parentWidget
        self._selectedModLoader = selectedModLoader
        self._buttonRect = buttonRect

        # run setup functions
        self._createButtonWidget()
        self._createMenuWidget()

    def clickDropdownOption(self, index):
        if 0 <= index < len(self._menuWidget.actions()):
            self._changeModLoader(index)

    def getSelectedModLoader(self):
        return self._modLoaderList[self._selectedModLoader]

    def getButtonWidget(self):
        return self._buttonWidget
    
    def getMenuWidget(self):
        return self._menuWidget

    def _createButtonWidget(self):
        # create font for button
        buttonFont = QtGui.QFont()
        buttonFont.setPointSize(14)
        
        # create button
        self._buttonWidget = QtWidgets.QPushButton(parent=self._parentWidget)
        self._buttonWidget.setGeometry(self._buttonRect)
        self._buttonWidget.setFont(buttonFont)
        self._buttonWidget.setText(self._modLoaderList[self._selectedModLoader] + " ▾")

        # making the lambda its own function doesn't work for some reason
        self._buttonWidget.clicked.connect(
            lambda : self._menuWidget.exec(
                self._buttonWidget.mapToGlobal(self._buttonWidget.rect().bottomLeft())))
        
    def _createMenuWidget(self):
        # create dropdown menu
        self._menuWidget = QtWidgets.QMenu(self._parentWidget)

        # add priority levels to action list
        i = 0
        for modLoader in self._modLoaderList:
            self._menuWidget.addAction(self._modLoaderList[i],
                                        lambda index=i : self._changeModLoader(index))
            i += 1

    def _changeModLoader(self, index):
        self._selectedModLoader = index
        self._buttonWidget.setText(self._modLoaderList[self._selectedModLoader] + " ▾")


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