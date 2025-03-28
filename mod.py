class ModPriority(object):
    def __init__(self, newName = "New Priority Level", red = 255, green = 255, blue = 255):
        self.name = newName
        self.redColorValue = red
        self.greenColorValue = green
        self.blueColorValue = blue

class Mod(object):
    def __init__(self, modName = "Untitled Mod", modID = -1, modVersions = ["No versions found"],
                 modPriority = ModPriority(), fromModrinth = False, fromCurseforge = False):
        self.__name = modName
        self.__ID = modID
        self.__versions = modVersions
        self.__priority = modPriority
        self.__modrinth = fromModrinth
        self.__curseforge = fromCurseforge

    def getName(self):
        return self.__name
    
    def getID(self):
        return self.__ID

    def getCurrentVersion(self):
        return self.__versions[0]

    def getVersionList(self):
        return self.__versions
    
    def getPriorityLevel(self):
        return self.__priority

    def _getCurrentVersion(self):
        pass

    def _getVersions(self):
        pass
    
    def _getModID(self):
        pass
