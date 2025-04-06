from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import mod

class ModTable():
    # How long the table is, in pixels
    _tableLength = 1000
    # How tall the table is, in pixels
    _tableHeight = 900
    # Height of the headings
    _headingHeight = 40

    # Number of columns in the table
    _numColumns = 3
    # Names of the columns
    _columnNames = ["Mod Name", "Latest Version", "Ready/Priority"]
    # Widths of the columns
    _columnWidths = [500, 170, 285]
    # Height of the rows
    _rowHeight = 50

    # The font size for everything in the table
    _fontSize = 14

    # The PyQt6 table widget we are managing
    _tableWidget:QtWidgets.QTableWidget
    # The parent object this widget is attached to
    _parentWidget:QtWidgets.QWidget
    # The list of mod to display
    _modList:list[mod.Mod]
    # The list of priority levels
    _priorityList:list[mod.ModPriority]
    # The selected version for this profile
    _selectedVersion:str
    
    def __init__(self, parent:QtWidgets.QWidget, modList:list[mod.Mod], priorityList:list[mod.ModPriority],
                 selectedVersion:str, reloadFunc):
        self._parentWidget = parent
        self._modList = modList
        self._priorityList = priorityList
        self._selectedVersion = selectedVersion
        self._reloadFunc = reloadFunc
        self._createTable()
        self.loadTable()

    def loadTable(self):
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

    def reloadTableRow(self, rowNum):
        self._setTableRow(rowNum, self._modList[rowNum])

    def getModList(self):
        return self._modList
    
    def setModList(self, newList):
        self._modList = newList
    # create and configure table
    def _createTable(self):
        self._tableWidget = QtWidgets.QTableWidget(self._parentWidget)
        self._tableWidget.setGeometry(QtCore.QRect(0, 0, self._tableLength, self._tableHeight))
        self._tableWidget.setObjectName("tableWidget")
        self._tableWidget.setColumnCount(self._numColumns)
    
    
    # adds a row to the table with the proper mod information
    def _setTableRow(self, rowNum, mod):
        for col in range(self._numColumns):
            # set the font size
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(self._fontSize)
            item.setFont(font)

            # Set the correct text for each item in the row
            match col:
                case 0:
                    item.setText(mod.getName())
                case 1:
                    item.setText(mod.getCurrentVersion())
                case 2:
                    # create dropdown button and put add it to this table item
                    self._createDropdownBtn(rowNum, mod)

            #apply changes
            self._tableWidget.setItem(rowNum, col, item)

    # creates all the buttons that reveal the priority dropdown menu
    def _createDropdownBtn(self, rowNum, mod):
        dropdownBtn = DropdownBtn(self._parentWidget, mod, self._priorityList, self._reloadFunc,
                                  rowNum, mod.getCurrentVersion() == self._selectedVersion, self._fontSize)
        self._tableWidget.setCellWidget(rowNum, 2, dropdownBtn.getButtonWidget())

    # Getters
    def getRowName(self, rowNum:int):
        return self._tableWidget.item(rowNum, 0).text()
    
    def getRowVersion(self, rowNum:int):
        return self._tableWidget.item(rowNum, 1).text()

    def getRowPriority(self, rowNum:int):
        return self._tableWidget.cellWidget(rowNum, 2).text()


class DropdownBtn():
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
        self._refreshFunc(self._rowNum, refreshEverything)

    def _showColorPicker(self):
        inputStr, okPressed = QtWidgets.QInputDialog.getText(self._parentWidget,
                                                  "Create new priority level", "Priority name:")
        
        if okPressed:
            selectedColor = QtWidgets.QColorDialog.getColor()
            if (selectedColor.isValid()):
                self._addModPriority(inputStr, selectedColor)

    def _addModPriority(self, modName:str, color:QtGui.QColor):
        self._priorityList.append(mod.ModPriority(modName, color=color))
        self._changeModPriority(len(self._priorityList) - 1, True)
    
    def getButtonWidget(self):
        return self._buttonWidget

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

    def __init__(self, parent: QtWidgets.QWidget, modList: list[mod.Mod], selectedVersion: str):
        # Assign variables
        self._parentWidget = parent
        self._modList = modList
        self._selectedVersion = selectedVersion

        self._series = QtCharts.QPieSeries()
        self._chartView = QtCharts.QChartView(parent=self._parentWidget)
        self._chartView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._chartView.setGeometry(QtCore.QRect(1000, 50, 900, 900))

        self.loadChart()

    def loadChart(self):
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
        chart.setTitleBrush(QtGui.QBrush(QtGui.QColor("white")))

        # Hide legend and set background color
        chart.legend().hide()
        chart.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

        # Update the existing chart view
        self._chartView.setChart(chart)

    def _calculateSliceSizes(self):
        self._sliceSizes = {self._readySlice: 0}
        for mod in self._modList:
            if mod.getCurrentVersion() == self._selectedVersion:
                self._sliceSizes[self._readySlice] += 1
            else:
                if mod.priority in self._sliceSizes:
                    self._sliceSizes[mod.priority] += 1
                else:
                    self._sliceSizes[mod.priority] = 1

    def _createSeries(self):
        label_font = QtGui.QFont()
        label_font.setPointSize(self._labelFontSize)

        # Create and populate chart series
        if not self._series.isEmpty():
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
            slice.setLabelColor(QtGui.QColor("white"))
            i += 1
