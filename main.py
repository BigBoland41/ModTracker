import sys, detailsWindow
from PyQt6 import QtWidgets
from testData import TestData

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    data = TestData()
    mainWindow = QtWidgets.QMainWindow()
    profileView = detailsWindow.DetailsWindow(
        mainWindow, data.constructModList(),
        data.priorityList, data.selectedVersion)
    mainWindow.showMaximized()
    sys.exit(app.exec())