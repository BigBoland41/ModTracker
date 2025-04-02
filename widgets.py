from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import mod

class ModTable():
    # How long the table is, in pixels
    __tableLength = 1000
    # How tall the table is, in pixels
    __tableHeight = 900
    # Height of the headings
    __headingHeight = 40

    # Number of columns in the table
    __numColumns = 3
    # Names of the columns
    __columnNames = ["Mod Name", "Latest Version", "Ready/Priority"]
    # Widths of the columns
    __columnWidths = [500, 170, 285]
    # Height of the rows
    __rowHeight = 50

    # The font size for everything in the table
    __fontSize = 14

    # The parent object this widget is attached to
    __parentWidget:QtWidgets.QWidget
    # The list of mod to display
    __modList:list[mod.Mod]
    # The list of priority levels
    __priorityList:list[mod.ModPriority]
    # The selected version for this profile
    __selectedVersion:str
    
    def __init__(self, parent:QtWidgets.QWidget, modList:list[mod.Mod], priorityList:list[mod.ModPriority],
                 selectedVersion:str, reloadFunc):
        self.__parentWidget = parent
        self.__modList = modList
        self.__priorityList = priorityList
        self.__selectedVersion = selectedVersion
        self.__reloadFunc = reloadFunc
        self.__createTable()
        self.loadTable()

    def loadTable(self):
        # set the row count to make the amount of mods in the list
        self.__tableWidget.setRowCount(len(self.__modList))

        # prepare font
        font = QtGui.QFont()
        font.setPointSize(self.__fontSize)
        self.__tableWidget.setFont(font)

        # configure headings
        for col in range(self.__numColumns):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(18)
            item.setFont(font)
            item.setText(self.__columnNames[col])
            self.__tableWidget.setHorizontalHeaderItem(col, item)
            self.__tableWidget.setColumnWidth(col, self.__columnWidths[col])

        # add rows to table and set row height
        for row in range(len(self.__modList)):
            self.__setTableRow(row, self.__modList[row])
            self.__tableWidget.setRowHeight(row, self.__rowHeight)

    def reloadTableRow(self, rowNum):
        self.__setTableRow(rowNum, self.__modList[rowNum])

    def getModList(self):
        return self.__modList
    
    # create and configure table
    def __createTable(self):
        self.__tableWidget = QtWidgets.QTableWidget(self.__parentWidget)
        self.__tableWidget.setGeometry(QtCore.QRect(0, 0, self.__tableLength, self.__tableHeight))
        self.__tableWidget.setObjectName("tableWidget")
        self.__tableWidget.setColumnCount(self.__numColumns)
    
    # adds a row to the table with the proper mod information
    def __setTableRow(self, rowNum, mod):
        for col in range(self.__numColumns):
            # set the font size
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(self.__fontSize)
            item.setFont(font)

            # Set the correct text for each item in the row
            match col:
                case 0:
                    item.setText(mod.getName())
                case 1:
                    item.setText(mod.getCurrentVersion())
                case 2:
                    # create dropdown button and put add it to this table item
                    self.__createDropdownBtn(rowNum, mod)

            #apply changes
            self.__tableWidget.setItem(rowNum, col, item)

    # creates all the buttons that reveal the priority dropdown menu
    def __createDropdownBtn(self, rowNum, mod):
        dropdownBtn = DropdownBtn(self.__parentWidget, mod, self.__priorityList, self.__reloadFunc,
                                  rowNum, mod.getCurrentVersion() == self.__selectedVersion, self.__fontSize)
        self.__tableWidget.setCellWidget(rowNum, 2, dropdownBtn.getButtonWidget())

class DropdownBtn():
    __parentWidget:QtWidgets.QWidget
    __buttonWidget:QtWidgets.QPushButton
    __menuWidget:QtWidgets.QMenu
    __mod:mod.Mod
    __priorityList:list[mod.ModPriority]
    __rowNum:int
    __fontSize:int

    def __init__(self, parentWidget:QtWidgets.QWidget, mod:mod.Mod, priorityList:list[mod.ModPriority],
                 refreshFunc, rowNum:int, isReady:bool, fontSize:int):
        # set attributes
        self.__parentWidget = parentWidget
        self.__mod = mod
        self.__priorityList = priorityList
        self.__refreshFunc = refreshFunc
        self.__rowNum = rowNum
        self.__fontSize = fontSize

        # run setup functions
        self.__createButtonWidget()
        self.__createMenuWidget()
        self.__customizeAppearance(isReady)

    def __createButtonWidget(self):
        # create button
        self.__buttonWidget = QtWidgets.QPushButton(parent=self.__parentWidget)

        # making the lambda its own function doesn't work for some reason
        self.__buttonWidget.clicked.connect(
            lambda : self.__menuWidget.exec(
                self.__buttonWidget.mapToGlobal(self.__buttonWidget.rect().bottomLeft())))
        
    def __createMenuWidget(self):
        # create dropdown menu
        self.__menuWidget = QtWidgets.QMenu(self.__parentWidget)

        # add priority levels to action list
        i = 0
        for priorityLevel in self.__priorityList:
            self.__menuWidget.addAction(priorityLevel.name,
                                        lambda index=i : self.__changeModPriority(index))
            i += 1
        self.__menuWidget.addAction("Add Priority Level", self.__showColorPicker)

    def __customizeAppearance(self, isReady:bool):
        # If the mod version matches the selected version...
        if (isReady):
            # set color to green and set text to ready
            backgroundColor = QtGui.QColor(0, 255, 0)
            self.__buttonWidget.setText("Ready")
        else:
            # set color to priority level color and set text to priority level name
            backgroundColor = self.__mod.priority.color
            self.__buttonWidget.setText(self.__mod.priority.name)
        
        # set the background color the one chosen above
        self.__buttonWidget.setStyleSheet(f"background-color: {backgroundColor.name()};"
                                          + f"color: black;"
                                          + f"font-size: {self.__fontSize}px;")

    def __changeModPriority(self, index, refreshEverything = False):
        self.__mod.priority = self.__priorityList[index]
        self.__refreshFunc(self.__rowNum, refreshEverything)

    def __showColorPicker(self):
        inputStr, okPressed = QtWidgets.QInputDialog.getText(self.__parentWidget,
                                                  "Create new priority level", "Priority name:")
        
        if okPressed:
            selectedColor = QtWidgets.QColorDialog.getColor()
            if (selectedColor.isValid()):
                self.__addModPriority(inputStr, selectedColor)

    def __addModPriority(self, modName:str, color:QtGui.QColor):
        self.__priorityList.append(mod.ModPriority(modName, color=color))
        self.__changeModPriority(len(self.__priorityList) - 1, True)
    
    def getButtonWidget(self):
        return self.__buttonWidget

class PieChart():
    __parentWidget: QtWidgets.QWidget
    __modList: list[mod.Mod]
    __selectedVersion: str

    __chartView: QtCharts.QChartView
    __series: QtCharts.QPieSeries
    __readySlice = mod.ModPriority("Ready", 0, 255, 0)
    __sliceSizes = {__readySlice: 0}

    __titleFontSize = 24
    __labelFontSize = 14

    def __init__(self, parent: QtWidgets.QWidget, modList: list[mod.Mod], selectedVersion: str):
        # Assign variables
        self.__parentWidget = parent
        self.__modList = modList
        self.__selectedVersion = selectedVersion

        self.__series = QtCharts.QPieSeries()
        self.__chartView = QtCharts.QChartView(parent=self.__parentWidget)
        self.__chartView.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.__chartView.setGeometry(QtCore.QRect(1000, 50, 900, 900))

        self.loadChart()

    def loadChart(self):
        # Calculate the size of each slice
        self.__calculateSliceSizes()

        # Create chart and add pie slices to it
        chart = QtCharts.QChart()
        self.__createSeries()
        chart.addSeries(self.__series)

        # Create title text
        title_font = QtGui.QFont()
        title_font.setPointSize(self.__titleFontSize)
        chart.setTitle('Mod Priority Chart')
        chart.setTitleFont(title_font)
        chart.setTitleBrush(QtGui.QBrush(QtGui.QColor("white")))

        # Hide legend and set background color
        chart.legend().hide()
        chart.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

        # Update the existing chart view
        self.__chartView.setChart(chart)

    def __calculateSliceSizes(self):
        self.__sliceSizes = {self.__readySlice: 0}
        for mod in self.__modList:
            if mod.getCurrentVersion() == self.__selectedVersion:
                self.__sliceSizes[self.__readySlice] += 1
            else:
                if mod.priority in self.__sliceSizes:
                    self.__sliceSizes[mod.priority] += 1
                else:
                    self.__sliceSizes[mod.priority] = 1

    def __createSeries(self):
        label_font = QtGui.QFont()
        label_font.setPointSize(self.__labelFontSize)

        # Create and populate chart series
        if not self.__series.isEmpty():
            self.__series.clear()

        i = 0
        for priority, count in self.__sliceSizes.items():
            self.__series.append(priority.name, count)
            slice = self.__series.slices()[i]

            if priority == self.__readySlice:
                slice.setExploded()

            slice.setColor(priority.color)
            slice.setBorderColor(priority.color)

            slice.setLabelVisible()
            slice.setLabelFont(label_font)
            slice.setLabelColor(QtGui.QColor("white"))
            i += 1
