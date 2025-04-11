import sys, unittest, detailsWindow, mod
from PyQt6 import QtWidgets
from testData import TestData

class TestDropdownBtn(unittest.TestCase):
    def setUp(self):
        # self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._detailsView = detailsWindow.DetailsWindow(self._window)
        self._data = TestData()

    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()
        # self._app.quit()

    def testChangeModPriority_Ready(self):
        modIndex = 0

        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()

        oldPriority = modTable.getRowDropdownBtnText(modIndex)
        if oldPriority is None:
            self.fail(
                "Attempted to access a row in the mod table that doesn't exist! " +
                f"Index accessed: {modIndex}. Number of table rows: {modTable.getNumRows()}"
            )

        dropdownBtn = modTable.getRowDropdownBtn(modIndex)

        if oldPriority == "Ready":
            dropdownBtn.clickDropdownOption(0)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Ready")
        elif oldPriority == "Low Priority":
            dropdownBtn.clickDropdownOption(0)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "High Priority")
        elif oldPriority == "High Priority":
            dropdownBtn.clickDropdownOption(1)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Low Priority")

    def testChangeModPriority_NotReady(self):
        modIndex = 1

        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()

        oldPriority = modTable.getRowDropdownBtnText(modIndex)
        if oldPriority is None:
            self.fail(
                "Attempted to access a row in the mod table that doesn't exist! " +
                f"Index accessed: {modIndex}. Number of table rows: {modTable.getNumRows()}"
            )

        dropdownBtn = modTable.getRowDropdownBtn(modIndex)

        if oldPriority == "Ready":
            dropdownBtn.clickDropdownOption(0)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Ready")
        elif oldPriority == "Low Priority":
            dropdownBtn.clickDropdownOption(0)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "High Priority")
        elif oldPriority == "High Priority":
            dropdownBtn.clickDropdownOption(1)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Low Priority")

    # TO DO: Uncomment and implement this test
    # def testAddModPriority(self):
    #     modIndex = 1

    #     self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
    #     modTable = self._detailsView.getModTable()

    #     oldPriority = modTable.getRowDropdownBtnText(modIndex)
    #     if oldPriority is None:
    #         self.fail(
    #             "Attempted to access a row in the mod table that doesn't exist! " +
    #             f"Index accessed: {modIndex}. Number of table rows: {modTable.getNumRows()}"
    #         )

    #     dropdownBtn = modTable.getRowDropdownBtn(modIndex)

    #     if oldPriority == "Ready":
    #         dropdownBtn.clickDropdownOption(0)
    #         self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Ready")
    #     elif oldPriority == "Low Priority":
    #         dropdownBtn.clickDropdownOption(0)
    #         self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "High Priority")
    #     elif oldPriority == "High Priority":
    #         dropdownBtn.clickDropdownOption(1)
    #         self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Low Priority")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2, failfast=True)