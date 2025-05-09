import sys, windows, widgets, mod
from PyQt6 import QtWidgets
from testData import TestData
import load

if __name__ == "__main__":
    # create app
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    windowManager = windows.WindowManager(mainWindow)
    '''
    # create test data
    data = TestData()
    jsonModList = load.createModList()
    jsonProfile = mod.ModProfile(jsonModList, data.priorityList, data.selectedVersion, "JSON mods")

    customModList = [
        mod.Mod("Sodium", 0, data._versionList5, mod.ModPriority("High Priority", 255, 85, 0)),
        mod.Mod("More Nether Mod", 0, data._versionList0, mod.ModPriority("Low Priority", 255, 255, 0))
    ]
    customProfile = mod.ModProfile(customModList, data.priorityList, data.selectedVersion, "mods I manually added in main.py because I'm lazy")

    # add test data
    windowManager.addProfile(jsonProfile)
    windowManager.addProfile(customProfile)
    '''
    profiles = load.createProfileList()
    for profile in profiles:
        windowManager.addProfile(profile)
    # show window and configure exit button
    mainWindow.showMaximized()
    sys.exit(app.exec())