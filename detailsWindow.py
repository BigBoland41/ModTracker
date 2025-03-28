import sys
from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts
import data
import mod

class DetailsWindow(object):
    # priority object to represent the mods that are ready
    __readySlice = mod.ModPriority("Ready", 0, 255, 0)
    # Each priority level : how many mods are that priority
    __pieChartSlices = {__readySlice: 0}
    # Names of the columns
    __tableColumns = ["Mod Name", "Latest Version", "Ready/Priority"]
    # Widths of the columns
    __tableWidths = [500, 180, 300]
    
    # Constructor. Creates window and runs functions to create widgets
    def __init__(self, modList, selectedVersion):
        # assign variables
        self.__modList = modList
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
        self.__tableWidget.setGeometry(QtCore.QRect(0, 0, 1000, 900))
        self.__tableWidget.setObjectName("tableWidget")
        self.__tableWidget.setColumnCount(3)
        self.__tableWidget.setRowCount(5)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.__tableWidget.setFont(font)

        # configure headings
        for col in range(len(self.__tableColumns)):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(18)
            item.setFont(font)
            item.setText(QtCore.QCoreApplication.translate("MainWindow", self.__tableColumns[col]))
            self.__tableWidget.setHorizontalHeaderItem(col, item)
            self.__tableWidget.setColumnWidth(col, self.__tableWidths[col])

        # add rows to table and set row height
        for row in range(len(self.__modList)):
            self.__addTableRow(row, self.__modList[row])
            self.__tableWidget.setRowHeight(row, 50)
    
    # adds a row to the table with the proper mod information
    def __addTableRow(self, rowNum, mod):
        for col in range(len(self.__tableColumns)):
            # set the font size to 14
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(14)
            item.setFont(font)

            # Set the correct text for each item in the row
            match col:
                case 0:
                    item.setText(QtCore.QCoreApplication.translate("MainWindow", mod.getName()))
                case 1:
                    item.setText(QtCore.QCoreApplication.translate("MainWindow", mod.getCurrentVersion()))
                case 2:
                    # If the mod version matches the selected version...
                    if (mod.getCurrentVersion() == self.__selectedVersion):
                        # set color to green and set text to ready
                        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
                        item.setText(QtCore.QCoreApplication.translate("MainWindow", "Ready"))
                        self.__pieChartSlices[self.__readySlice] += 1
                    else:
                        # add to pie chart dictionary for later
                        priority = mod.getPriorityLevel()
                        if (priority in self.__pieChartSlices):
                            self.__pieChartSlices[priority] += 1
                        else:
                            self.__pieChartSlices[priority] = 1

                        # set color to priority level color and set text to priority level name
                        brush = QtGui.QBrush(QtGui.QColor(
                            priority.redColorValue,
                            priority.greenColorValue,
                            priority.blueColorValue))
                        item.setText(QtCore.QCoreApplication.translate("MainWindow", priority.name))
                    
                    # set background color
                    brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                    item.setBackground(brush)

                    # make the text black by changing the foreground style to solid pattern
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                    item.setForeground(brush)

            #apply changes
            self.__tableWidget.setItem(rowNum, col, item)

    # creates the pie chart with the proper priority information
    def __createPieChart(self):
        # prepare font sizes
        title_font = QtGui.QFont()
        title_font.setPointSize(24)
        label_font = QtGui.QFont()
        label_font.setPointSize(14)
        
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
        self.__addModTextField.setText(QtCore.QCoreApplication.translate("MainWindow", "Enter mod URL here"))

    # creates the add mod button,
    # which the user can click to add the mod they've input into the add mod text field.
    def __createAddModBtn(self):
        self.__addModBtn = QtWidgets.QPushButton(parent=self.__centralwidget)
        self.__addModBtn.setGeometry(QtCore.QRect(800, 910, 200, 70))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.__addModBtn.setFont(font)
        self.__addModBtn.setObjectName("addModBtn")
        self.__addModBtn.clicked.connect(self.__addMod)
        self.__addModBtn.setText(QtCore.QCoreApplication.translate("MainWindow", "Add Mod"))

    # Adds a mod to the profile. Triggered when the add mod button is clicked.
    def __addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self.__addModTextField.text()  # this gets the input from the text field
        print(inputString)

        data.mod_info(data.mod_lookup(inputString))
        pass

# Main function for testing: open a mock profile with mock information
if __name__ == "__main__":
    highPriority = mod.ModPriority("High Priority", 255, 85, 0)
    lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
    modList = [mod.Mod("Sodium", 123456, ["1.21.5","1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Lithium", 123456, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("Entity Culling", 123456, ["1.21.4","1.21.3","1.21.2", "1.21.1", "1.21"], highPriority),
               mod.Mod("CIT Resewn", 123456, ["1.21.1", "1.21"], lowPriority),
               mod.Mod("Animatica", 123456, ["1.21"], lowPriority)]
    profileView = DetailsWindow(modList, "1.21.5")