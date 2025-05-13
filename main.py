import sys, os, windows, ctypes
from PyQt6 import QtWidgets, QtGui

if __name__ == "__main__":
    # set app ID
    myappid = u'modtracker' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # create app
    print("Starting app")
    app = QtWidgets.QApplication(sys.argv)

    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    icon_path = os.path.join(base_path, "icon.ico")

    icon = QtGui.QIcon(icon_path)
    if (not icon.isNull()):
        app.setWindowIcon(icon)
    else:
        print("App icon could not be found.")

    mainWindow = QtWidgets.QMainWindow()

    # create UI and load from data from json file
    windowManager = windows.WindowManager(mainWindow, processEventsFunc=lambda : app.processEvents())

    # show window and close temporary loading window
    print("Done! Displaying window")
    mainWindow.showMaximized()
    sys.exit(app.exec())