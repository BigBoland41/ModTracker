import sys, windows, widgets, mod
from PyQt6 import QtWidgets
from testData import TestData

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    data = TestData()
    mainWindow = QtWidgets.QMainWindow()
    windows.configureWindow(mainWindow)

    stackedWidget = QtWidgets.QStackedWidget(mainWindow)
    stackedWidget.setGeometry(mainWindow.geometry())
    mainWindow.setCentralWidget(stackedWidget)

    jsonModList = widgets.createModList()
    jsonProfile = mod.ModProfile(jsonModList, data.priorityList, data.selectedVersion, "JSON mods")

    customModList = [
        mod.Mod("Sodium", 0, data._versionList5, mod.ModPriority("High Priority", 255, 85, 0)),
        mod.Mod("More Nether Mod", 0, data._versionList0, mod.ModPriority("Low Priority", 255, 255, 0))
    ]
    customProfile = mod.ModProfile(customModList, data.priorityList, data.selectedVersion, "manually added mods")

    profileList = [
        jsonProfile,
        customProfile
    ]

    profileSelectView = windows.ProfileSelectWindow(stackedWidget, profileList, data.priorityList)
    stackedWidget.addWidget(profileSelectView)

    mainWindow.showMaximized()
    sys.exit(app.exec())