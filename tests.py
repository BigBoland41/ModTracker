import unittest, sys, widgets
from PyQt6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widgets.setFontelloPath()
    testSuite = unittest.TestLoader().discover('tests', pattern='test_*.py')
    unittest.TextTestRunner().run(testSuite)

    # known issue: tests.py crashes after completing testSuite