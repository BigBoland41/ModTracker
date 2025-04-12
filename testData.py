import mod

class TestData(object):
    # applies to any test making an API call, not just the testAPICalls class
    # it's recommended you turn this off if you plan to run tests multiple
    # times in a row, in order to not get our API calls denied.
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

        return modList