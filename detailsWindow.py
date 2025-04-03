import sys, data, mod, widgets
from PyQt6 import QtCore, QtGui, QtWidgets

class DetailsWindow(object):
    __modList:list[mod.Mod]
    __priorityList:list[mod.ModPriority]
    
    __tableWidget:QtWidgets.QTableWidget
    __pieChartWidget:widgets.PieChart
    
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
        
        self.__pieChartWidget = widgets.PieChart(self.__centralwidget, self.__modList, self.__selectedVersion)
        self.__tableWidget = widgets.ModTable(self.__centralwidget, self.__modList, self.__priorityList,
                                              self.__selectedVersion, self.__reloadWidgetsSingle)

        self.__createAddModTextField()
        self.__createAddModBtn()

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

    def __reloadWidgets(self, rowNum, reloadEverything = False):
        self.__pieChartWidget.loadChart()
        if (reloadEverything):
            self.__tableWidget.loadTable()
        else:
            self.__tableWidget.reloadTableRow(rowNum)

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

    # Adds a mod to the profile. Triggered when the add mod button is clicked.
    def __addMod(self):
        # When the button is clicked, this function will run. Add your code here
        inputString = self.__addModTextField.text()  # this gets the input from the text field
        print(inputString)

        newMod = mod.Mod(url = inputString, modPriority=mod.ModPriority("Low Priority", 255, 255, 0))
        self.__modList.append(newMod)
        self.__tableWidget.setModList(self.__modList)
        #print(self.__tableWidget.getModList()[0])
        self.__reloadWidgets()

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
    newList = []
    profileView = DetailsWindow(modList, priorityList, "1.21.5")