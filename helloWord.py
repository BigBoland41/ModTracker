import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(50, 50, 1000, 500)
    window.setWindowTitle("Mod Tracker")

    label = QLabel(window)
    label.setText("Mod Tracker")
    label.move(10, 10)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()