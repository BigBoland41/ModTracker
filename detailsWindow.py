import sys
from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import data
import mod

class DetailsWindow(object):
    # priority object to represent the mods that are ready
    __readySlice = mod.ModPriority("Ready", 0, 255, 0)
    # Each priority level : how many mods are that priority
    __pieChartSlices = {__readySlice: 0}

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

    # The font size of nearly all text 
    __generalFontSize = 14
    
    # Constructor. Creates window and runs functions to create widgets
    def __init__(self, modList, priorityList, selectedVersion):
        # assign variables
        self.__modList = modList
        self.__priorityList = priorityList
        self.__selectedVersion = selectedVersion

        # create app and window
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()

        # run setup functions
        self.__configureWindow(MainWindow)
        self.__createWidgets()

        # finish setup
        MainWindow.showMaximized()
        sys.exit(app.exec())
        
    # configures the window, including name, size, and status bar
    def __configureWindow(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Mod Tracker")
        MainWindow.resize(1000, 500)
        self.__centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.__centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.__centralwidget)
        self.__statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.__statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.__statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # creates all widgets by running their create functions
    def __createWidgets(self):
        self.__createTable()
        self.__createPieChart()
        self.__createAddModTextField()
        self.__createAddModBtn()

    # creates the table displaying all the mods in this profile
    def __createTable(self):
        # create and configure table
        self.__tableWidget = QtWidgets.QTableWidget(parent=self.__centralwidget)
        self.__tableWidget.setGeometry(QtCore.QRect(0, 0, self.__tableLength, self.__tableHeight))
        self.__tableWidget.setObjectName("tableWidget")
        self.__tableWidget.setColumnCount(self.__numColumns)
        self.__tableWidget.setRowCount(len(self.__modList))
        font = QtGui.QFont()
        font.setPointSize(self.__generalFontSize)
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
            # self.__createDropdownBtn(row, self.__modList[row])
    
    # adds a row to the table with the proper mod information
    def __setTableRow(self, rowNum, mod):
        for col in range(self.__numColumns):
            # set the font size
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(self.__generalFontSize)
            item.setFont(font)

            # Set the correct text for each item in the row
            match col:
                case 0:
                    item.setText(mod.getName())
                case 1:
                    item.setText(mod.getCurrentVersion())
                case 2:
                    # add to pie chart dictionary for later
                    isReady = mod.getCurrentVersion() == self.__selectedVersion
                    if (isReady):
                        self.__pieChartSlices[self.__readySlice] += 1
                        if (mod.priority in self.__pieChartSlices):
                            self.__pieChartSlices[mod.priority] += 1
                        else:
                            self.__pieChartSlices[mod.priority] = 1
                    
                    # create dropdown button and put add it to this table item
                    self.__createDropdownBtn(rowNum, mod, isReady)

            #apply changes
            self.__tableWidget.setItem(rowNum, col, item)

    # creates the pie chart with the proper priority information
    def __createPieChart(self):
        # prepare font sizes
        title_font = QtGui.QFont()
        title_font.setPointSize(24)
        label_font = QtGui.QFont()
        label_font.setPointSize(self.__generalFontSize)
        
        # create and populate chart series
        series = QtCharts.QPieSeries()
        i = 0
        for priority, count in self.__pieChartSlices.items():
            series.append(priority.name, count)
            slice = series.slices()[i]
            if (priority == self.__readySlice):
                slice.setExploded()
            slice.setColor(QtGui.QColor(
                priority.redColorValue,
                priority.greenColorValue,
                priority.blueColorValue))
            slice.setBorderColor(QtGui.QColor(
                priority.redColorValue,
                priority.greenColorValue,
                priority.blueColorValue))
            slice.setLabelVisible()
            slice.setLabelFont(label_font)
            slice.setLabelColor(QtGui.QColor("white"))
            i += 1

        # create chart 
        chart = QtCharts.QChart()
        chart.addSeries(series)

        chart.setTitle('Mod Priority Chart')
        chart.setTitleFont(title_font)
        chart.setTitleBrush(QtGui.QBrush(QtGui.QColor("white")))

        chart.legend().hide()
        chart.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

        chart_view = QtCharts.QChartView(chart, parent=self.__centralwidget)
        chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        chart_view.setGeometry(QtCore.QRect(1000, 50, 900, 900))
    
    # creates the add mod text input field,
    # where the user can input the URL of the mod they want to add.
    def __createAddModTextField(self):
        self.__addModTextField = QtWidgets.QLineEdit(parent=self.__centralwidget)
        self.__addModTextField.setGeometry(QtCore.QRect(0, 910, 800, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__addModTextField.setFont(font)
        self.__addModTextField.setObjectName("addModTextField")
        self.__addModTextField.setText("Enter mod URL here")

    # creates the add mod button
    # which the user can click to add the mod they've input into the add mod text field.
    def __createAddModBtn(self):
        self.__addModBtn = QtWidgets.QPushButton(parent=self.__centralwidget)
        self.__addModBtn.setGeometry(QtCore.QRect(800, 910, 200, 70))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.__addModBtn.setFont(font)
        self.__addModBtn.setObjectName("addModBtn")
        self.__addModBtn.clicked.connect(self.__addMod)
        self.__addModBtn.setText("Add Mod")

    # creates all the buttons that reveal the priority dropdown menu
    def __createDropdownBtn(self, rowNum, mod, isReady):
        dropdownBtn = DropdownBtn(self.__centralwidget, mod, self.__priorityList,
                                  self.__setTableRow, rowNum, isReady, self.__generalFontSize)
        self.__tableWidget.setCellWidget(rowNum, 2, dropdownBtn.getButtonWidget())

    # Adds a mod to the profile. Triggered when the add mod button is clicked.
    def __addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self.__addModTextField.text()  # this gets the input from the text field
        print(inputString)

        data.mod_info(data.mod_lookup(inputString))

class DropdownBtn():
    __buttonWidget:QtWidgets.QPushButton
    __menuWidget:QtWidgets.QMenu
    __mod:mod.Mod
    __priorityList:list[mod.ModPriority]
    __rowNum:int
    __fontSize:int

    def __init__(self, parentWidget, mod:mod.Mod, priorityList:list[mod.ModPriority],
                 refreshFunc, rowNum:int, isReady:bool, fontSize:int):
        self.__mod = mod
        self.__priorityList = priorityList
        self.__refreshFunc = refreshFunc
        self.__rowNum = rowNum
        self.__fontSize = fontSize

        # create button
        self.__buttonWidget = QtWidgets.QPushButton(parent=parentWidget)

        # making the lambda its own function doesn't work for some reason
        self.__buttonWidget.clicked.connect(
            lambda : self.__menuWidget.exec(
                self.__buttonWidget.mapToGlobal(self.__buttonWidget.rect().bottomLeft())))

        self.__menuWidget = QtWidgets.QMenu(parentWidget)

        i = 0
        for priorityLevel in self.__priorityList:
            self.__menuWidget.addAction(priorityLevel.name,
                                        lambda index=i : self.__changeModPriority(index))
            i += 1

        self.__customizeAppearance(isReady)

    def __customizeAppearance(self, isReady:bool):
        # If the mod version matches the selected version...
        if (isReady):
            # set color to green and set text to ready
            backgroundColor = QtGui.QColor(0, 255, 0)
            self.__buttonWidget.setText("Ready")
        else:
            # set color to priority level color and set text to priority level name
            backgroundColor = QtGui.QColor(
                self.__mod.priority.redColorValue,
                self.__mod.priority.greenColorValue,
                self.__mod.priority.blueColorValue)
            self.__buttonWidget.setText(self.__mod.priority.name)
        
        # set the background color the one chosen above
        self.__buttonWidget.setStyleSheet(f"background-color: {backgroundColor.name()};"
                                          + f"color: black;"
                                          + f"font-size: {self.__fontSize}px;")

    def __changeModPriority(self, index):
        self.__mod.priority = self.__priorityList[index]
        self.__refreshFunc(self.__rowNum, self.__mod)
    
    def getButtonWidget(self):
        return self.__buttonWidget

# Main function for testing: open a mock profile with mock information
if __name__ == "__main__":
    highPriority = mod.ModPriority("High Priority", 255, 85, 0)
    lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
    priorityList = [highPriority, lowPriority]
    modList = [mod.Mod("Sodium", 1, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Lithium", 2, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Entity Culling", 3, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("Dynamic FPS", 4, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("Enhanced Block Entities", 5, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Entity Model Features", 6, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Entity Texture Features", 7, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("CIT Resewn", 8, ["1.21.1", "1.21"], lowPriority),
               mod.Mod("Animatica", 9, ["1.21"], lowPriority),
               mod.Mod("Continuity", 10, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Iris Shaders", 11, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("WI Zoom", 12, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("LambDynamicLights", 13, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("MaLiLib", 14, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Litematica", 15, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("MniHUD", 16, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("WorldEdit", 17, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Flashback", 18, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("Shulker Box Tooltip", 19, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("CraftPresence", 20, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("Command Keys", 21, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("Advancements Reloaded", 22, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               mod.Mod("Mod Menu", 23, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], lowPriority),
               ]
    profileView = DetailsWindow(modList, priorityList, "1.21.5")