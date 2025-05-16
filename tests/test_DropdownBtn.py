import sys, os, unittest
from PyQt6 import QtWidgets, QtGui

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import windows
from testData import TestData

class TestDropdownBtn(unittest.TestCase):
    def setUp(self):
        # self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._detailsView = windows.DetailsWindow()
        self._data = TestData()

    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()
        # self._app.quit()

    def testChangeModPriority(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()

        for i in range(modTable.getNumRows()):
            oldPriority = modTable.getRowDropdownBtnText(i)
            if oldPriority is None:
                self.fail(
                    "Attempted to access a row in the mod table that doesn't exist! " +
                    f"Index accessed: {i}. Number of table rows: {modTable.getNumRows()}"
                )

            dropdownBtn = modTable.getRowDropdownBtn(i)

            if oldPriority == "Ready":
                dropdownBtn.clickDropdownOption(0)
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Ready")
            elif oldPriority == "Low Priority":
                dropdownBtn.clickDropdownOption(0)
                self.assertEqual(modTable.getRowDropdownBtnText(i), "High Priority")
            elif oldPriority == "High Priority":
                dropdownBtn.clickDropdownOption(1)
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Low Priority")

    def testAddModPriority(self):
        newPriorityName = "New Priority"
        newPriorityColor = QtGui.QColor(255, 255, 255)

        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()
        for i in range(modTable.getNumRows()):
            oldPriority = modTable.getRowDropdownBtnText(i)
            if oldPriority is None:
                self.fail(
                    "Attempted to access a row in the mod table that doesn't exist! " +
                    f"Index accessed: {i}. Number of table rows: {modTable.getNumRows()}"
                )

            modTable.getRowDropdownBtn(i).clickDropdownOption(2, newPriorityName, newPriorityColor)

            if oldPriority == "Ready":
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Ready")
            else:
                self.assertEqual(modTable.getRowDropdownBtnText(i), newPriorityName)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2, failfast=True)