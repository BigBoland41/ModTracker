from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import mod, os

_btnFontSize = 18
_specialSymbolFontSize = 16
_labelFontSize = 12

_fontelloPath:str


# Represents the first cell of a row in the mod table. Displays the mod's name and "open link in browser" icon, as well as holds the mod object.
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
    _dropdownBtnList:list['PriorityDropdownBtn'] = []
     
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

        item.setText(mod.getName())  # This text won't appear, but it's useful for testing
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
        dropdownBtn = PriorityDropdownBtn(self._parentWidget, mod, priorityList, self._reloadFunc, rowNum, isReady, self._fontSize)
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
    _priorityList:list[mod.ModPriority]
    # The selected version for this profile
    _selectedVersion:str
    
    def __init__(self, parent:QtWidgets.QWidget, modList:list[mod.Mod], priorityList:list[mod.ModPriority], selectedVersion:str, reloadFunc, saveFunc):
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