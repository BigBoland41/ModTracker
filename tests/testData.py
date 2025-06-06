import sys, os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import mod

class TestData(object):
    # applies to any test making an API call, not just the testAPICalls class
    # it's recommended you turn this off if you plan to run tests many
    # times in a row, in order to not get our API calls denied or throttled.
    testAPICalls = True

    selectedVersion = "1.21.5"
    highPriority = mod.ModPriority("High Priority", 255, 85, 0)
    lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
    priorityList = [highPriority, lowPriority]

    _versionList5 = ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"]
    _versionList4 = ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"]
    _versionList1 = ["1.21", "1.21.1"]
    _versionList0 = ["1.21"]

    modNames = [
        "Sodium", "Lithium", "Entity Culling", "Dynamic FPS", "Enhanced Block Entities",
        "Entity Model Features", "Entity Texture Features", "CIT Resewn", "Animatica",
        "Continuity", "Iris Shaders", "WI Zoom", "LambDynamicLights", "MaLiLib", "Litematica",
        "MiniHUD", "WorldEdit", "Flashback", "Shulker Box Tooltip", "CraftPresence",
        "Command Keys", "Advancements Reloaded", "Mod Menu"
    ]

    _modVersions = [
        _versionList5, _versionList4, _versionList4, _versionList5, _versionList4, _versionList4,
        _versionList4, _versionList1, _versionList0, _versionList4, _versionList5, _versionList5,
        _versionList5, _versionList4, _versionList4, _versionList4, _versionList4, _versionList4,
        _versionList4, _versionList4, _versionList5, _versionList4, _versionList5
    ]

    _modPriorities = [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    
    def constructModList(self):
        modList = []
        for i in range(len(self.modNames)):
            match self._modPriorities[i]:
                case 0:
                    modList.append(mod.Mod(self.modNames[i], i, self._modVersions[i], self.highPriority))
                case 1:
                    modList.append(mod.Mod(self.modNames[i], i, self._modVersions[i], self.lowPriority))
        
        return modList
    
    def getModPriority(self, index:int):
        match self._modPriorities[index]:
            case 0:
                return self.highPriority
            case 1:
                return self.lowPriority
            
    def getModCurrentVersion(self, index:int):
        return self._modVersions[index][-1]
    
    def old_initMockData(window):
        highPriority = mod.ModPriority("High Priority", 255, 85, 0)
        lowPriority = mod.ModPriority("Low Priority", 255, 255, 0)
        
        modList = [
            mod.Mod("Sodium", 1, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority, url = "https://modrinth.com/mod/sodium"),
            mod.Mod("Lithium", 2, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/lithium"),
            mod.Mod("Entity Culling", 3, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority, url = "https://modrinth.com/mod/entityculling"),
            mod.Mod("Dynamic FPS", 4, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority, url = "https://modrinth.com/mod/dynamic-fps"),
            mod.Mod("Enhanced Block Entities", 5, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/ebe"),
            mod.Mod("Entity Model Features", 6, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/entity-model-features"),
            mod.Mod("Entity Texture Features", 7, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/entitytexturefeatures"),
            mod.Mod("CIT Resewn", 8, ["1.21", "1.21.1"], lowPriority, url = "https://modrinth.com/mod/cit-resewn"),
            mod.Mod("Animatica", 9, ["1.21"], lowPriority, url = "https://modrinth.com/mod/animatica"),
            mod.Mod("Continuity", 10, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/continuity"),
            mod.Mod("Iris Shaders", 11, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority, url = "https://modrinth.com/mod/iris"),
            mod.Mod("WI Zoom", 12, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority, url = "https://modrinth.com/mod/wi-zoom"),
            mod.Mod("LambDynamicLights", 13, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], highPriority, url = "https://modrinth.com/mod/lambdynamiclights"),
            mod.Mod("MaLiLib", 14, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/malilib"),
            mod.Mod("Litematica", 15, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/litematica"),
            mod.Mod("MniHUD", 16, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/mod/minihud"),
            mod.Mod("WorldEdit", 17, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], highPriority, url = "https://modrinth.com/plugin/worldedit"),
            mod.Mod("Flashback", 18, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority, url = "https://modrinth.com/mod/flashback"),
            mod.Mod("Shulker Box Tooltip", 19, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority, url = "https://modrinth.com/mod/shulkerboxtooltip"),
            mod.Mod("CraftPresence", 20, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority, url = "https://modrinth.com/mod/craftpresence"),
            mod.Mod("Command Keys", 21, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority, url = "https://modrinth.com/mod/commandkeys"),
            mod.Mod("Advancements Reloaded", 22, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4"], lowPriority, url = "https://modrinth.com/mod/advancements-reloaded"),
            mod.Mod("Mod Menu", 23, ["1.21","1.21.1","1.21.2","1.21.3", "1.21.4", "1.21.5"], lowPriority, url = "https://modrinth.com/mod/modmenu")
        ]

        return modList