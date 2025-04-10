import sys, mod, unittest, detailsWindow
from PyQt6 import QtWidgets, QtTest, QtCore

_testAPICalls = True

def runTests(testAPICalls=True):
    global _testAPICalls
    _testAPICalls = testAPICalls
    unittest.main()

class testPieChart(unittest.TestCase):
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
        self._window.__init__
        self._app.quit()
    
    def test1_EmptyWindow(self):
        self._detailsView = detailsWindow.DetailsWindow(self._window)
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        self.assertEqual(len(sliceList), 1)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 0)

    def test2_PrepopulatedWindow(self):
        self._detailsView = detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        self.assertEqual(len(sliceList), 3)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 7)
        self.assertEqual(chart.getSliceSizes().get(sliceList[1]), 9)
        self.assertEqual(chart.getSliceSizes().get(sliceList[2]), 7)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def test3_AddMod_ReadyEmpty(self):
        self._detailsView = detailsWindow.DetailsWindow(self._window)
        chart = self._detailsView.getPieChart()
        sliceList = list(chart.getSliceSizes().keys())

        addModTextField = self._window.findChild(QtWidgets.QLineEdit, "addModTextField")
        addModBtn = self._window.findChild(QtWidgets.QPushButton, "addModBtn")

        QtTest.QTest.keyClicks(addModTextField, "https://modrinth.com/mod/sodium")
        QtTest.QTest.mouseClick(addModBtn, QtCore.Qt.MouseButton.LeftButton)

        self.assertEqual(len(sliceList), 1)
        self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 1)

    @unittest.skipIf(not _testAPICalls, "API tests are off")
    def test4_AddMod_ReadyPrepopulated(self):
        self._detailsView = detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
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
    def test5_AddMod_PreExistingPriority(self):
        self._detailsView = detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
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

#     @unittest.skipIf(not _testAPICalls, "API tests are off")
#     def test6_AddMod_NewPriority(self):
#         self._app = QtWidgets.QApplication(sys.argv)
#         self._window = QtWidgets.QMainWindow()
#         self._detailsView = detailsWindow.DetailsWindow(self._window)
#         chart = self._detailsView.getPieChart()
#         sliceList = list(chart.getSliceSizes().keys())

#         self._detailsView.setAddModTextFieldText("https://modrinth.com/mod/nether-height-expansion-mod")
#         self._detailsView.clickAddModBtn()

#         self.assertEqual(len(sliceList), 1)
#         self.assertEqual(chart.getSliceSizes().get(sliceList[0]), 0)
#         with self.assertRaises(IndexError):
#             self.assertEqual(chart.getSliceSizes().get(sliceList[1]), 1)

if __name__ == "__main__":
    runTests()