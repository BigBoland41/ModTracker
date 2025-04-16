import sys, detailsWindow, widgets
from PyQt6 import QtWidgets
from testData import TestData

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    data = TestData()
    mainWindow = QtWidgets.QMainWindow()
    mods = widgets.createModList()
    profileView = detailsWindow.DetailsWindow(
        mainWindow, mods,
        data.priorityList, data.selectedVersion)
    mainWindow.showMaximized()
    sys.exit(app.exec())