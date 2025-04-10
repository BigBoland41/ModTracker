import sys, mod, unittest, detailsWindow
from PyQt6 import QtWidgets, QtTest, QtCore

_testAPICalls = True

def runTests(testAPICalls=True):
    global _testAPICalls
    _testAPICalls = testAPICalls
    unittest.main()

class testModTable(unittest.TestCase):
    _selectedVersion = "1.21.5"
    _highPriority = mod.ModPriority("High Priority", 255, 85, 0)
    _lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
    _priorityList = [_highPriority, _lowPriority]
        
    _modNames = [
        "Sodium",
        "Lithium",
        "Entity Culling",
        "Dynamic FPS",
        "Enhanced Block Entities",
        "Entity Model Features",
        "Entity Texture Features",
        "CIT Resewn",
        "Animatica",
        "Continuity",
        "Iris Shaders",
        "WI Zoom",
        "LambDynamicLights",
        "MaLiLib",
        "Litematica",
        "MiniHUD",
        "WorldEdit",
        "Flashback",
        "Shulker Box Tooltip",
        "CraftPresence",
        "Command Keys",
        "Advancements Reloaded",
        "Mod Menu"
    ]

    _modVersions = [
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21", "1.21.1"],
        ["1.21"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"],
        ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"]
    ]

    _modPriorities = [0,0,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1]

    _modCurrentVersions = [
                "1.21.5",
                "1.21.4",
                "1.21.4",
                "1.21.5",
                "1.21.4",
                "1.21.4",
                "1.21.4",
                "1.21.1",
                "1.21",
                "1.21.4",
                "1.21.5",
                "1.21.5",
                "1.21.5",
                "1.21.4",
                "1.21.4",
                "1.21.4",
                "1.21.4",
                "1.21.4",
                "1.21.4",
                "1.21.4",
                "1.21.5",
                "1.21.4",
                "1.21.5"
            ]

    def _constructModList(self):
        modList = []
        for i in range(len(self._modNames)):
            match self._modPriorities[i]:
                case 0:
                    modList.append(mod.Mod(
                        self._modNames[i], i, self._modVersions[i],self._highPriority
                    ))
                case 1:
                    modList.append(mod.Mod(
                        self._modNames[i], i, self._modVersions[i], self._lowPriority
                    ))
        
        return modList
    
    def setUp(self):
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()

    def tearDown(self):
        self._app.quit()
    
    def _getModPriority(self, index:int):
        match self._modPriorities[index]:
            case 0:
                return self._highPriority
            case 1:
                return self._lowPriority
    
    def test1_ModNameText(self):
        self._detailsView =  detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
        modTable = self._detailsView.getModTable()

        for i in range(len(self._modNames)):
            self.assertEqual(modTable.getRowNameText(i), self._modNames[i])

    def test2_ModVersionsText(self):
        self._detailsView =  detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
        modTable = self._detailsView.getModTable()

        for i in range(len(self._modNames)):
            self.assertEqual(modTable.getRowVersionText(i), self._modCurrentVersions[i])

    def test3_ModPriorityText(self):
        self._detailsView =  detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
        modTable = self._detailsView.getModTable()

        for i in range(len(self._modNames)):
            if self._modCurrentVersions[i] == self._selectedVersion:
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Ready")
            else:
                self.assertEqual(modTable.getRowDropdownBtnText(i), self._getModPriority(i).name)

    def test4_ModReady(self):
        self._detailsView =  detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
        modTable = self._detailsView.getModTable()

        for i in range(len(self._modCurrentVersions)):
            self.assertEqual(modTable.getRowVersionText(i), self._modCurrentVersions[i])

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def test5_AddMod(self):
        self._detailsView = detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )

        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        addModTextField = self._window.findChild(QtWidgets.QLineEdit, "addModTextField")
        addModBtn = self._window.findChild(QtWidgets.QPushButton, "addModBtn")

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/sodium")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/nether-height-expansion-mod")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

        self.assertEqual(modTable.getNumRows(), oldNumRows + 2)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def test6_AddMod_EmptyTable(self):
        self._detailsView = detailsWindow.DetailsWindow(self._window)

        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        addModTextField = self._window.findChild(QtWidgets.QLineEdit, "addModTextField")
        addModBtn = self._window.findChild(QtWidgets.QPushButton, "addModBtn")

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/sodium")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/nether-height-expansion-mod")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

        self.assertEqual(modTable.getNumRows(), oldNumRows + 2)

    def test7_RemoveMod(self):
        self._detailsView = detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )

        modTable = self._detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        nextRowName = modTable.getRowNameText(11)
        deleteBtn = modTable.getRowDeleteBtn(10)

        QtTest.QTest.mouseClick(deleteBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(modTable.getRowNameText(10), nextRowName)
        self.assertEqual(modTable.getNumRows(), oldNumRows - 1)

if __name__ == "__main__":
    runTests()