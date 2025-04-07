import sys, mod, unittest, json, detailsWindow
from PyQt6 import QtWidgets

class testAPICalls(unittest.TestCase):

    def testMod(self):
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
    _modList:list[mod.Mod]
    _selectedVersion = "1.21.5"
    
    def initDetailsView(self, window):
        highPriority = mod.ModPriority("High Priority", 255, 85, 0)
        lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
        priorityList = [highPriority, lowPriority]

        self._modList = [
            mod.Mod("Sodium", 1, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
            mod.Mod("Lithium", 2, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Entity Culling", 3, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Dynamic FPS", 4, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
            mod.Mod("Enhanced Block Entities", 5, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Entity Model Features", 6, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Entity Texture Features", 7, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("CIT Resewn", 8, ["1.21", "1.21.1"], lowPriority),
            mod.Mod("Animatica", 9, ["1.21"], lowPriority),
            mod.Mod("Continuity", 10, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Iris Shaders", 11, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
            mod.Mod("WI Zoom", 12, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
            mod.Mod("LambDynamicLights", 13, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
            mod.Mod("MaLiLib", 14, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Litematica", 15, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("MniHUD", 16, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("WorldEdit", 17, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Flashback", 18, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Shulker Box Tooltip", 19, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("CraftPresence", 20, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Command Keys", 21, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
            mod.Mod("Advancements Reloaded", 22, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Mod Menu", 23, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority)
        ]

        return detailsWindow.DetailsWindow(window, self._modList, priorityList, self._selectedVersion)
    
    def testCreateWindow_Prepopulated(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)

        self.assertIsNotNone(detailsView)
    
    def testModNameText(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(self._modList)):
            self.assertEqual(modTable.getRowNameText(i), self._modList[i].getName())
    
    def testModVersionsText(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(self._modList)):
            self.assertEqual(modTable.getRowVersionText(i), self._modList[i].getCurrentVersion())

    def testModPriorityText(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(self._modList)):
            if self._modList[i].getCurrentVersion() == self._selectedVersion:
                self.assertEqual(modTable.getRowDropdownBtnText(i), "Ready")
            else:
                self.assertEqual(modTable.getRowDropdownBtnText(i), self._modList[i].priority.name)
    
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
        
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        for i in range(len(correctVersions)):
            self.assertEqual(modTable.getRowVersionText(i), correctVersions[i])

    def testAddMod(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/sodium")
        detailsView.clickAddModBtn()

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/nether-height-expansion-mod")
        detailsView.clickAddModBtn()

        modTable = detailsView.getModTable()

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

    def testCreateWindow_Empty(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = detailsWindow.DetailsWindow(mainWindow)

        self.assertIsNotNone(detailsView)

    def testAddMod_EmptyTable(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = detailsWindow.DetailsWindow(mainWindow)

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/sodium")
        detailsView.clickAddModBtn()

        detailsView.setAddModTextFieldText("https://modrinth.com/mod/nether-height-expansion-mod")
        detailsView.clickAddModBtn()

        modTable = detailsView.getModTable()
        
        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 2), "Sodium")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 2), "1.21.5")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 2), "Ready")

        self.assertEqual(modTable.getRowNameText(modTable.getNumRows() - 1), "More Nether Mod")
        self.assertEqual(modTable.getRowVersionText(modTable.getNumRows() - 1), "1.21")
        self.assertEqual(modTable.getRowDropdownBtnText(modTable.getNumRows() - 1), "High Priority")

    def testRemoveMod(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        secondRowName = modTable.getRowNameText(1)
        modTable.clickRowDeleteBtn(0)
        self.assertEqual(modTable.getRowNameText(0), secondRowName)

class testDropdownBtn(unittest.TestCase):
    _modList:list[mod.Mod]
    _selectedVersion = "1.21.5"
    
    def initDetailsView(self, window):
        highPriority = mod.ModPriority("High Priority", 255, 85, 0)
        lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
        priorityList = [highPriority, lowPriority]

        self._modList = [
            mod.Mod("Sodium", 1, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
            mod.Mod("Lithium", 2, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Entity Culling", 3, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Dynamic FPS", 4, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
            mod.Mod("Enhanced Block Entities", 5, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Entity Model Features", 6, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Entity Texture Features", 7, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("CIT Resewn", 8, ["1.21", "1.21.1"], lowPriority),
            mod.Mod("Animatica", 9, ["1.21"], lowPriority),
            mod.Mod("Continuity", 10, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Iris Shaders", 11, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
            mod.Mod("WI Zoom", 12, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
            mod.Mod("LambDynamicLights", 13, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority),
            mod.Mod("MaLiLib", 14, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Litematica", 15, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("MniHUD", 16, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("WorldEdit", 17, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority),
            mod.Mod("Flashback", 18, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Shulker Box Tooltip", 19, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("CraftPresence", 20, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Command Keys", 21, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority),
            mod.Mod("Advancements Reloaded", 22, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority),
            mod.Mod("Mod Menu", 23, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority)
        ]

        return detailsWindow.DetailsWindow(window, self._modList, priorityList, self._selectedVersion)
    
    def testChangeModPriority(self):
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = QtWidgets.QMainWindow()
        detailsView = self.initDetailsView(mainWindow)
        modTable = detailsView.getModTable()

        self.assertEqual(modTable.getRowDropdownBtnText(1), "High Priority")
        modTable.changeRowPriority(1, 1)
        self.assertEqual(modTable.getRowDropdownBtnText(1), "Low Priority")
    
if __name__ == "__main__":
    unittest.main()