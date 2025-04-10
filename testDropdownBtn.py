import sys, unittest, detailsWindow, mod
from PyQt6 import QtWidgets

def runTests():
    unittest.main()

class testDropdownBtn(unittest.TestCase):
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

    def testChangeModPriority(self):
        modIndex = 1

        self._detailsView = detailsWindow.DetailsWindow(
            self._window, self._constructModList(), self._priorityList, self._selectedVersion
        )
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

if __name__ == "__main__":
    runTests()