import sys, mod, unittest, detailsWindow
from PyQt6 import QtWidgets

def runTests():
    unittest.main()

class testdetailsView(unittest.TestCase):
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
    
    def testCreateWindow_Prepopulated(self):
        self._detailsView =  detailsWindow.DetailsWindow(
            self._window, self._constructModList(),
            self._priorityList, self._selectedVersion
        )

        self.assertIsNotNone(self._detailsView)

    def testCreateWindow_Empty(self):
        self._detailsView = detailsWindow.DetailsWindow(self._window)

        self.assertIsNotNone(self._detailsView)

if __name__ == "__main__":
    runTests()