import sys, unittest, windows
from PyQt6 import QtWidgets, QtTest, QtCore
from testData import TestData

_testAPICalls = True

class TestModTable(unittest.TestCase):
    def setUp(self):
        # self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._detailsView = windows.DetailsWindow(self._window)
        self._data = TestData()

        global _testAPICalls
        _testAPICalls = self._data.testAPICalls

    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()
        # self._app.quit()
    
    def testModNameText(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()

        for i in range(len(self._data.modNames)):
            self.assertEqual(modTable.getRowNameText(i), self._data.modNames[i])

    def testModVersionsText(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()

        for i in range(len(self._data.modNames)):
            self.assertEqual(modTable.getRowVersionText(i), self._data.getModCurrentVersion(i))

    def testModPriorityText(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()

        for i in range(len(self._data.modNames)):
            if self._data.getModCurrentVersion(i) == self._data.selectedVersion:
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Ready")
            else:
                self.assertEqual(modTable.getRowDropdownBtnText(i), self._data.getModPriority(i).name)

    def testModReady(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        modTable = self._detailsView.getModTable()
        modTable.saveModList()
        for i in range(len(self._data.modNames)):
            self.assertEqual(modTable.getRowVersionText(i), self._data.getModCurrentVersion(i))

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testAddMod(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)

        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        self._detailsView.enterAndAddMod("https://modrinth.com/mod/sodium")
        self._detailsView.enterAndAddMod("https://modrinth.com/mod/nether-height-expansion-mod")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

        self.assertEqual(modTable.getNumRows(), oldNumRows + 2)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testAddMod_EmptyTable(self):
        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        self._detailsView.enterAndAddMod("https://modrinth.com/mod/sodium")
        self._detailsView.enterAndAddMod("https://modrinth.com/mod/nether-height-expansion-mod")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

        self.assertEqual(modTable.getNumRows(), oldNumRows + 2)

    def testRemoveMod(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)

        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        nextRowName = modTable.getRowNameText(11)
        deleteBtn = modTable.getRowDeleteBtn(10)

        QtTest.QTest.mouseClick(deleteBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(modTable.getRowNameText(10), nextRowName)
        self.assertEqual(modTable.getNumRows(), oldNumRows - 1)

    def testRemoveAllMods(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)

        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()
        for i in range(modTable.getNumRows()):
            deleteBtn = modTable.getRowDeleteBtn(0)
            QtTest.QTest.mouseClick(deleteBtn, QtCore.Qt.MouseButton.LeftButton)
            self.assertEqual(modTable.getNumRows(), oldNumRows - i - 1)
        
        self.assertEqual(modTable.getNumRows(), 0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2,failfast=True)