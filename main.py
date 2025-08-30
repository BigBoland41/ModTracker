import sys, os, windows, ctypes, widgets
from PyQt6 import QtWidgets, QtGui

if __name__ == "__main__":
    # set app ID
    # myappid = u'modtracker' # arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # create app
    print("Starting app")
    app = QtWidgets.QApplication(sys.argv)

    # Check if running as a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # set app icon
    icon_path = os.path.join(base_path, "icon.ico")
    icon = QtGui.QIcon(icon_path)
    
    # set reference to Fontello
    widgets.setFontelloPath()

    mainWindow = QtWidgets.QMainWindow()

    if (not icon.isNull()):
        app.setWindowIcon(icon)
        mainWindow.setWindowIcon(icon)
    else:
        print("App icon could not be found.")

    # create UI and load from data from json file
    windowManager = windows.WindowManager(mainWindow, processEventsFunc=lambda : app.processEvents())

    # show window and close temporary loading window
    print("Done! Displaying window")
    mainWindow.showMaximized()
    sys.exit(app.exec())