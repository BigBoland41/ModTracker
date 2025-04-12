import sys, mod, unittest, detailsWindow
from PyQt6 import QtWidgets, QtTest, QtCore, QtGui
from testData import TestData

_testAPICalls = True

class TestPieChart(unittest.TestCase):
    def setUp(self):
        # self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._detailsView = detailsWindow.DetailsWindow(self._window)
        self._data = TestData()

        global _testAPICalls
        _testAPICalls = self._data.testAPICalls

    def tearDown(self):
        self._window.deleteLater()
        self._detailsView.getModList().clear()
        self._detailsView.getModTable()._dropdownBtnList.clear()
        # self._app.quit()
    
    def testEmptyWindow(self):
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        self.assertEqual(len(sliceList), 1)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 0)

    def testPrepopulatedWindow(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        self.assertEqual(len(sliceList), 3)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 7)
        self.assertEqual(chart.getSliceSizes().get(sliceList[1]), 9)
        self.assertEqual(chart.getSliceSizes().get(sliceList[2]), 7)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testAddMod_ReadyEmpty(self):
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        addModTextField = self._window.findChild(QtWidgets.QLineEdit, "addModTextField")
        addModBtn = self._window.findChild(QtWidgets.QPushButton, "addModBtn")

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/sodium")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(len(sliceList), 1)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 1)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testAddMod_ReadyPrepopulated(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        addModTextField = self._window.findChild(QtWidgets.QLineEdit, "addModTextField")
        addModBtn = self._window.findChild(QtWidgets.QPushButton, "addModBtn")

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/sodium")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(len(sliceList), 3)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 8)
        self.assertEqual(chart.getSliceSizes().get(sliceList[1]), 9)
        self.assertEqual(chart.getSliceSizes().get(sliceList[2]), 7)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def testAddMod_PreExistingPriority(self):
        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        addModTextField = self._window.findChild(QtWidgets.QLineEdit, "addModTextField")
        addModBtn = self._window.findChild(QtWidgets.QPushButton, "addModBtn")

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/nether-height-expansion-mod")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(self._detailsView.getModTable().getNumRows(), 24)

        self.assertEqual(len(sliceList), 3)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 7)
        self.assertEqual(chart.getSliceSizes().get(sliceList[1]), 10)
        self.assertEqual(chart.getSliceSizes().get(sliceList[2]), 7)

    def testAddNewPriority(self):
        newPriorityName = "New Priority"
        newPriorityColor = QtGui.QColor(255, 255, 255)

        self._detailsView.loadNewData(self._data.constructModList(), self._data.priorityList, self._data.selectedVersion)
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())
        modTable = self._detailsView.getModTable()

        for modIndex in range(0, 2):
            # priorityName = newPriorityName + f" {modIndex}"
            sliceList = list(chart.getSliceSizes().keys())

            oldPriority = modTable.getRowDropdownBtnText(modIndex)
            oldSliceLength = len(sliceList)
            oldSliceSizes = []
            for i in range(len(sliceList)):
                oldSliceSizes.append(chart.getSliceSizes().get(sliceList[i]))
            
            modTable.getRowDropdownBtn(modIndex).clickDropdownOption(2, newPriorityName, newPriorityColor)

            sliceList = list(chart.getSliceSizes().keys())
            if oldPriority == "Ready":
                self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Ready")
                self.assertEqual(len(sliceList), oldSliceLength)
            else:
                self.assertEqual(modTable.getRowDropdownBtnText(modIndex), newPriorityName)
                self.assertEqual(len(sliceList), oldSliceLength + 1)
            self.assertEqual(modTable.getModList()[modIndex].priority.name, newPriorityName)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    unittest.main(verbosity=2)