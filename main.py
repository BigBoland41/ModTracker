import sys, windows, load
from PyQt6 import QtWidgets

if __name__ == "__main__":
    # create app
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    windowManager = windows.WindowManager(mainWindow)

    # load and insert profiles
    profiles = load.createProfileList()
    for profile in profiles:
        windowManager.addProfile(profile)

    # show window and configure exit button
    mainWindow.showMaximized()
    sys.exit(app.exec())