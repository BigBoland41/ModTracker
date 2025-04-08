import sys, mod, unittest, json, detailsWindow
from PyQt6 import QtWidgets

_testAPICalls = False

_selectedVersion = "1.21.5"
_highPriority = mod.ModPriority("High Priority", 255, 85, 0)
_lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
_priorityList = [_highPriority, _lowPriority]
_modList:list[mod.Mod] = [
        mod.Mod("Sodium", 1, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _highPriority),
        mod.Mod("Lithium", 2, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("Entity Culling", 3, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _lowPriority),
        mod.Mod("Dynamic FPS", 4, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _lowPriority),
        mod.Mod("Enhanced Block Entities", 5, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("Entity Model Features", 6, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("Entity Texture Features", 7, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("CIT Resewn", 8, ["1.21", "1.21.1"], _lowPriority),
        mod.Mod("Animatica", 9, ["1.21"], _lowPriority),
        mod.Mod("Continuity", 10, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("Iris Shaders", 11, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _lowPriority),
        mod.Mod("WI Zoom", 12, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _highPriority),
        mod.Mod("LambDynamicLights", 13, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _highPriority),
        mod.Mod("MaLiLib", 14, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("Litematica", 15, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("MniHUD", 16, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("WorldEdit", 17, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _highPriority),
        mod.Mod("Flashback", 18, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _lowPriority),
        mod.Mod("Shulker Box Tooltip", 19, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _lowPriority),
        mod.Mod("CraftPresence", 20, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _lowPriority),
        mod.Mod("Command Keys", 21, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _lowPriority),
        mod.Mod("Advancements Reloaded", 22, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], _lowPriority),
        mod.Mod("Mod Menu", 23, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], _lowPriority)
    ]

_globalApp:QtWidgets.QApplication

def _initDetailsView(window):
    return detailsWindow.DetailsWindow(window, _modList, _priorityList, _selectedVersion)

class testAPICalls(unittest.TestCase):
    def testMod(self):
        if not _testAPICalls:
            pass

        modObj = mod.Mod(url ="https://modrinth.com/mod/sodium")
        modObj2 = mod.Mod(url = "https://modrinth.com/mod/fabric-api")
        modObj3 = mod.Mod(url = "https://modrinth.com/mod/cloth-config")
        modObj4 = mod.Mod(url = "https://www.curseforge.com/minecraft/mc-mods/sodium")
        self.assertNotEqual(modObj.getModrinthData(), False)
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj.getCurseforgeData(), False)
        self.assertEqual(modObj.getID(), "AANobbMI")
        self.assertNotEqual(modObj2.getModrinthData(), False)
        self.assertEqual(modObj2.getCurrentVersion(), "25w14craftmine")
        self.assertNotEqual(modObj3.getModrinthData(), False)
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        with open("mod_info.json", "w") as json_file:
            json.dump(modObj.getCurseforgeData(), json_file, indent=4)
        self.assertNotEqual(modObj4.getModrinthData(), False)
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")
        self.assertNotEqual(modObj4.getCurseforgeData(), False)
        self.assertEqual(modObj4.getID(), "AANobbMI")
        self.assertEqual(modObj.getName(), "Sodium")
        self.assertEqual(modObj2.getName(), "Fabric API")
        self.assertEqual(modObj3.getName(), "Cloth Config API")
        self.assertEqual(modObj4.getName(), "Sodium")
        self.assertEqual(modObj.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj2.getCurrentVersion(), "25w14craftmine")
        self.assertEqual(modObj3.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj4.getCurrentVersion(), "1.21.5")
        self.assertEqual(modObj.getURL(), "https://modrinth.com/mod/sodium")
        self.assertEqual(modObj2.getURL(), "https://modrinth.com/mod/fabric-api")
        self.assertEqual(modObj3.getURL(), "https://modrinth.com/mod/cloth-config")
        self.assertEqual(modObj4.getURL(), "https://www.curseforge.com/minecraft/mc-mods/sodium")

class testDetailsView(unittest.TestCase):
    def testCreateWindow_Prepopulated(self):
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)

        self.assertIsNotNone(detailsView)
    
    def testModNameText(self):
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(_modList)):
            self.assertEqual(modTable.getRowNameText(i), _modList[i].getName())
    
    def testModVersionsText(self):
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(_modList)):
            self.assertEqual(modTable.getRowVersionText(i), _modList[i].getCurrentVersion())

    def testModPriorityText(self):
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(_modList)):
            if _modList[i].getCurrentVersion() == _selectedVersion:
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Ready")
            else:
                self.assertEqual(modTable.getRowDropdownBtnText(i), _modList[i].priority.name)
    
    def testModReady(self):
        correctVersions = [
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
        
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(correctVersions)):
            self.assertEqual(modTable.getRowVersionText(i), correctVersions[i])

    def testAddMod(self):
        if not _testAPICalls:
            pass
        
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)

        modTable = detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/sodium")
        detailsView.clickAddModBtn()

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/nether-height-expansion-mod")
        detailsView.clickAddModBtn()

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

        self.assertEqual(modTable.getNumRows(), oldNumRows + 2)

    def testCreateWindow_Empty(self):
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = detailsWindow.DetailsWindow(mainWindow)

        self.assertIsNotNone(detailsView)

    def testAddMod_EmptyTable(self):
        if not _testAPICalls:
            pass
        
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = detailsWindow.DetailsWindow(mainWindow)

        modTable = detailsView.getModTable()
        oldNumRows = modTable.getNumRows()
        
        detailsView.setAddModTextFieldText("https://modrinth.com/mod/sodium")
        detailsView.clickAddModBtn()

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/nether-height-expansion-mod")
        detailsView.clickAddModBtn()

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

        self.assertEqual(modTable.getNumRows(), oldNumRows + 2)

    def testRemoveMod(self):
        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)

        modTable = detailsView.getModTable()
        oldNumRows = modTable.getNumRows()

        nextRowName = modTable.getRowNameText(11)
        modTable.clickRowDeleteBtn(10)
        self.assertEqual(modTable.getRowNameText(10), nextRowName)

        self.assertEqual(modTable.getNumRows(), oldNumRows - 1)

'''
Due to some exotic issue with pyqt6 (probably multi-threading related), this test class has
a few issues that make it special for some reason. This comment block documents these issues,
as well as explain why there's a global QApplication object.

Firstly, the row being tested is a mod that isn't ready, the test will fail, but ONLY most
other tests are disabled (which tests affect is seemingly random. I just comment out all them).
If you want to change modIndex to a row that isn't ready, you will have to run each test in
isolation for it to pass.

Secondly, the test will try to access the DetailsWindow object from the most recently run test.
Which test this is isn't guaranteed, (because the order unit tests are run in isn't guaranteed),
but especially if it accesses the one from a test that manipulates the mod table, you can see some
unexpected results.

More importantly though, this seems to also happens with the QApplication, causing it to attempt
to access objects that have already been deleted. The solution to this is to use an QApplication
that has already been initalized, but because the other tests are running simultaneously and there
can only be one QApplication object at a time, all tests are required to use a global app. This
doesn't have any impact on other tests, but it's not "proper" way to do independent testing.
'''
class testDropdownBtn(unittest.TestCase):
    def testChangeModPriority(self):
        modIndex = 0

        # app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = _initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        oldPriority = modTable.getRowDropdownBtnText(modIndex)
        if (oldPriority == None):
            self.fail(
                "Attempted to access a row in the mod table that doesn't exist! " + 
                f"Index accessed: {modIndex}. Number of table rows: {modTable.getNumRows()}"
            )
        elif (oldPriority == "Ready"):
            modTable.getRowDropdownBtn(modIndex).clickDropdownOption(0)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Ready")
        elif (oldPriority == "Low Priority"):
            modTable.getRowDropdownBtn(modIndex).clickDropdownOption(0)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "High Priority")
        elif (oldPriority == "High Priority"):
            modTable.getRowDropdownBtn(modIndex).clickDropdownOption(1)
            self.assertEqual(modTable.getRowDropdownBtnText(modIndex), "Low Priority")


class testPieChart(unittest.TestCase):
    def test(self):
        pass

if __name__ == "__main__":
    _globalApp = QtWidgets.QApplication(sys.argv)
    unittest.main()