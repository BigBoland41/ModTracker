import sys, mod, unittest, windows
from PyQt6 import QtWidgets
from testData import TestData

class TestDetailsView(unittest.TestCase):
    def setUp(self):
        # self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._data = TestData()

    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()
        # self._app.quit()
    
    def testCreateWindow_Prepopulated(self):
        self._detailsView =  windows.DetailsWindow(
            self._window, self._data.constructModList(),
            self._data.priorityList, self._data.selectedVersion
        )

        self.assertIsNotNone(self._detailsView)
        self.assertEqual(self._detailsView.getModTable().getNumRows(), len(self._data.modNames))

    def testCreateWindow_Empty(self):
        self._detailsView = windows.DetailsWindow(self._window)

        self.assertIsNotNone(self._detailsView)
        self.assertEqual(self._detailsView.getModTable().getNumRows(), 0)

    def testCreateWindow_LoadNewData(self):
        self._detailsView = windows.DetailsWindow(self._window)
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)

        self.assertIsNotNone(self._detailsView)
        self.assertEqual(self._detailsView.getModTable().getNumRows(), len(self._data.modNames))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2,failfast=True)