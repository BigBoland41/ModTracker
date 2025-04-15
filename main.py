import sys, windows
from PyQt6 import QtWidgets
from testData import TestData

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    data = TestData()
    mainWindow = QtWidgets.QMainWindow()

    selectView = windows.ProfileSelectWindow(mainWindow)

    # profileView = windows.DetailsWindow(
    #     mainWindow, data.constructModList(),
    #     data.priorityList, data.selectedVersion)
    
    mainWindow.showMaximized()
    sys.exit(app.exec())