from PyQt6 import QtGui

class ModPriority(object):
    name:str
    color:QtGui.QColor

    def __init__(self, newName = "New Priority Level", red = 255, green = 255, blue = 255, color:QtGui.QColor = None):
        self.name = newName
        if color == None:
            self.color = QtGui.QColor(red, green, blue)
        else:
            self.color = color

class Mod(object):
    priority:ModPriority

    __name:str
    __ID:int
    __versions:list[str]
    __modrinth:bool
    __curseforge:bool
    
    def __init__(self, modName = "Untitled Mod", modID = -1, modVersions = ["No versions found"],
                 modPriority = ModPriority(), fromModrinth = False, fromCurseforge = False):
        self.__name = modName
        self.__ID = modID
        self.__versions = modVersions
        self.priority = modPriority
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

    def _getCurrentVersion(self):
        pass

    def _getVersions(self):
        pass
    
    def _getModID(self):
        pass
