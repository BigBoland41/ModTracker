import sys, windows
from PyQt6 import QtWidgets

if __name__ == "__main__":
    # create app
    print("Starting app")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()

    # create UI and load from data from json file
    windowManager = windows.WindowManager(mainWindow, processEventsFunc=lambda : app.processEvents())

    # show window and close temporary loading window
    print("Done! Displaying window")
    mainWindow.showMaximized()
    sys.exit(app.exec())