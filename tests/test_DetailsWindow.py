import sys, os, unittest
from PyQt6 import QtWidgets

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import windows
import testData

class TestDetailsView(testData.TestCase):
    createDetailsView = False

    def testCreateWindow_Prepopulated(self):
        self._detailsView =  windows.DetailsWindow(
            modList=self._data.constructModList(),
            priorityList=self._data.priorityList, selectedVersion=self._data.selectedVersion
        )

        self.assertIsNotNone(self._detailsView)
        self.assertEqual(self._detailsView.getModTable().getNumRows(), len(self._data.modNames))

    def testCreateWindow_Empty(self):
        self._detailsView = windows.DetailsWindow()

        self.assertIsNotNone(self._detailsView)
        self.assertEqual(self._detailsView.getModTable().getNumRows(), 0)

    def testCreateWindow_LoadNewData(self):
        self._detailsView = windows.DetailsWindow()
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)

        self.assertIsNotNone(self._detailsView)
        self.assertEqual(self._detailsView.getModTable().getNumRows(), len(self._data.modNames))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2,failfast=True)