import sys
from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUI(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec())

class Ui_MainWindow(object):
    def setupUI(self, MainWindow):
        self.configureWindow(MainWindow)
        self.createTable()
        self.createInputWidgets()
        self.createPieChart()
        self.setUIText(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def configureWindow(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    # generated with Qt Designer then modified by Stephen
    def createTable(self):
        # create and configure table
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1000, 900))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(5)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tableWidget.setFont(font)

        # configure headings
        for col in range(3):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(18)
            item.setFont(font)
            self.tableWidget.setHorizontalHeaderItem(col, item)

        # configure table tiems
        for row in range(5):
            for col in range(3):
                # set the font size to 14
                item = QtWidgets.QTableWidgetItem()
                font = QtGui.QFont()
                font.setPointSize(14)
                item.setFont(font)

                # for the last column...
                if (col == 2):
                    # change the background color to the appropriate color
                    # hardcoded for the sake of this prototype
                    match row:
                        case 1:
                            brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
                        case 3:
                            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
                        case _:
                            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
                    brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                    item.setBackground(brush)

                    # make the text black by changing the foreground style to solid pattern
                    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                    brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
                    item.setForeground(brush)

                #apply changes
                self.tableWidget.setItem(row, col, item)

        # resize the rows and columns
        self.setTableSizes()

    # generated with Qt Designer
    # fills each item in the table with the appropriate text
    def setUIText(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mod Tracker"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Mod Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Latest Version"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Ready/Priority"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "Sodium"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "1.21.4"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "Ready"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "Continuity"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("MainWindow", "1.20.6"))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("MainWindow", "High Priority"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "Entity Culling"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("MainWindow", "1.21.4"))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("MainWindow", "Ready"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("MainWindow", "Fabric Skyboxes"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("MainWindow", "1.21.1"))
        item = self.tableWidget.item(3, 2)
        item.setText(_translate("MainWindow", "Non-essential"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("MainWindow", "Enhanced Block Entities"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("MainWindow", "1.21.4"))
        item = self.tableWidget.item(4, 2)
        item.setText(_translate("MainWindow", "Ready"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.addModTextField.setText(_translate("MainWindow", "Enter mod URL here"))
        self.addModBtn.setText(_translate("MainWindow", "Add Mod"))
    
    def setTableSizes(self):
        # set column sizes
        self.tableWidget.setColumnWidth(0, 500)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 300)

        # set row sizes
        for col in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(col, 50)

    def createPieChart(self):
        # create and populate chart series
        self.series = QtCharts.QPieSeries()
        self.series.append('Ready', 3)
        self.series.append('High Priority', 1)
        self.series.append('Non-essential', 1)

        # create chart 
        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.series)

        # prepare font sizes
        title_font = QtGui.QFont()
        title_font.setPointSize(24)
        label_font = QtGui.QFont()
        label_font.setPointSize(14)

        self.slice = self.series.slices()[0]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setBrush(QtGui.QColor(0, 255, 0))
        self.slice.setLabelFont(label_font)
        self.slice.setLabelColor(QtGui.QColor("white"))

        self.slice = self.series.slices()[1]
        self.slice.setLabelVisible()
        self.slice.setBrush(QtGui.QColor(255, 85, 0))
        self.slice.setLabelFont(label_font)
        self.slice.setLabelColor(QtGui.QColor("white"))

        self.slice = self.series.slices()[2]
        self.slice.setLabelVisible()
        self.slice.setBrush(QtGui.QColor(255, 255, 0))
        self.slice.setLabelFont(label_font)
        self.slice.setLabelColor(QtGui.QColor("white"))

        self.chart.setTitle('Mod Priority Chart')
        self.chart.setTitleFont(title_font)
        self.chart.setTitleBrush(QtGui.QBrush(QtGui.QColor("white")))

        self.chart.legend().hide()
        self.chart.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

        self._chart_view = QtCharts.QChartView(self.chart, parent=self.centralwidget)
        self._chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._chart_view.setGeometry(QtCore.QRect(1000, 50, 900, 900))
    
    def createInputWidgets(self):
        self.addModTextField = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.addModTextField.setGeometry(QtCore.QRect(0, 910, 800, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addModTextField.setFont(font)
        self.addModTextField.setObjectName("addModTextField")

        self.addModBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addModBtn.setGeometry(QtCore.QRect(800, 910, 200, 70))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.addModBtn.setFont(font)
        self.addModBtn.setObjectName("addModBtn")
        self.addModBtn.clicked.connect(self.addMod)
    
    def addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self.addModTextField.text()  # this gets the input from the text field
        print(inputString)
        pass


if __name__ == "__main__":
    main()