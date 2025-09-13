from PyQt6 import QtGui
import callModrinth, callCurseForge, webbrowser

class ModPriority(object):
    name:str
    color:QtGui.QColor
    r:int
    g:int
    b:int

    def __init__(self, newName = "New Priority Level", red = 255, green = 255, blue = 255, color:QtGui.QColor = None):
        self.name = newName
        self.r = red
        self.g = green
        self.b = blue
        if color == None:
            self.color = QtGui.QColor(red, green, blue)
        else:
            self.color = color
            self.r = color.red()
            self.g = color.green()
            self.b = color.blue()

    def createDict(self):
        return {
            "name": self.name,
            "r":self.r,
            "g":self.g,
            "b":self.b
        }
        

    def __str__(self):
        return f"{self.name}"
    
    def __eq__(self, other):
        if not isinstance(other, ModPriority):
            return False
        elif self.name == other.name and self.r == other.r and self.g == other.g and self.b == other.b:
            return True
        else:
            return False
    
    # Ensure the object can be used as a dictionary key
    def __hash__(self):
        return hash((self.name, self.r, self.g, self.b))

class Mod(object):
    priority:ModPriority
    _name:str
    _url:str
    _ID:int
    _versions:list[str]
    _tablePosition:int

    _modrinthData:dict # False if uninitialized
    _curseforgeData:dict # False if uninitialized
    
    _curseforgeRegex = r"^https:\/\/(www\.)?curseforge\.com\/minecraft\/mc-mods\/[a-zA-Z0-9-_]+\/?$"
    _modrinthRegex = r"^https:\/\/(www\.)?modrinth\.com\/mod\/[a-zA-Z0-9-_]+\/?$"

    _requestTimeout = 10.0 # How many seconds to wait for an API call before timeout.
    
    # can pass mod info directly for testing, but can also just call constructor with a url and it will get all 
    # relevant info from the api and store it all
    def __init__(self, modName = "Untitled Mod", modID = -1, modVersions = ["No versions found"],
                 modPriority = ModPriority(), url = -1, tablePosition = -1, modrinthData = False, curseforgeData = False):
        self.priority = modPriority
        self._name = modName
        self._ID = modID
        self._url = url
        self._versions = modVersions
        self._tablePosition = tablePosition
        self._modrinthData = modrinthData
        self._curseforgeData = curseforgeData
        
        if(url != -1):
            self.refreshMod()

        if modrinthData:
            self._extractModrinth()
        elif curseforgeData:
            self._extractCurseforge()


    def __str__(self):
        return f"{self._name}, version: {self.getCurrentVersion()}, priority: {self.priority}"
    
    def __lt__(self, other):
        if self._tablePosition > 0 or other._tablePosition > 0:
            return self._tablePosition < other._tablePosition
        else:
            return self._name < other._name
        
    def __eq__(self, other):
        if not isinstance(other, Mod):
            return False
        else:
            return self._name == other._name and self._ID == other._ID and self._url == other._url and self._versions == other._versions

    # Getters
    def getName(self):
        return self._name
    
    def getID(self):
        return self._ID

    def getCurrentVersion(self):
        return self._versions[-1]
    
    def getVersionList(self):
        return self._versions
    
    def getURL(self):
        if self._url == -1:
            return None
        else:
            return self._url

    def getVersions(self):
        return self._versions
    
    def getModrinthData(self):
        return self._modrinthData
    
    def getCurseforgeData(self):
        return self._curseforgeData
    
    def getTablePosition(self):
        return self._tablePosition
    
    # A mod is considered valid if it has valid modrinth data or valid curseforge data
    def isValid(self):
        return self._modrinthData != False or self._curseforgeData != False
    
    # Verify if the URL this mod was initialized with is valid
    def verifyURL(self):
        curseforge = callModrinth.verifyURL(self._url)
        modrinth = callCurseForge.verifyURL(self._url)
        return modrinth or curseforge

    # Runs when the mod's data needs to be reset. Makes an API call and extracts the raw data
    def refreshMod(self):
        self.callAPIs()

        # Use the service the URL came from first, and if that fails, try the other service
        if callModrinth.verifyURL(self._url):
            if callModrinth.verifyURL(self._url):
                self._extractModrinth()
            else:
                self._extractCurseforge()
        elif callCurseForge.verifyURL(self._url):
            if callCurseForge.verifyURL(self._url):
                self._extractCurseforge()
            else:
                self._extractModrinth()

    # Use the URL this mod was initialized with to get its data from CurseForge and Modrinth
    def callAPIs(self):
        mod_slug = self._url.rstrip("/").split("/")[-1]
        
        if callModrinth.verifyURL(self._url):
            self._modrinthData = callModrinth.modData(mod_slug)
        
        if callCurseForge.verifyURL(self._url):
            self._curseforgeData = callCurseForge.modData(mod_slug)

    # Downloads the latest version of the mod. Returns True if a mod was downloaded and False if not.
    def downloadMod(self, loader:str, version:str, preventDownload=False):
        mod_slug = self._url.rstrip("/").split("/")[-1]
        downloadLink = False

        if self._modrinthData != False:
            downloadLink = callModrinth.downloadMod(mod_slug, loader, version)
        elif self._curseforgeData != False:
            downloadLink = callCurseForge.downloadMod(self._curseforgeData, self._ID, loader, version)

        if downloadLink != False:
            if preventDownload == False:
                webbrowser.open(downloadLink)
            return True
        else:
            return False

    # Returns mod information as a dictionary
    def createDict(self):
        return {
            "priority":self.priority.createDict(),
            "name" : self._name,
            "id" : self._ID,
            "url" : self._url,
            "versions" : self._versions,
            "tablePosition" : self._tablePosition,
        }

    # Extract modrinth json data from API call
    def _extractModrinth(self):
        if (self._modrinthData == False):
            return -1
        
        self._name = self._modrinthData["title"]
        self._ID = self._modrinthData["id"]
        self._versions = self._modrinthData["game_versions"]

    # Extract curseforge json data from API call and sort the version list
    def _extractCurseforge(self):
        if (self._curseforgeData == False):
            return -1
        
        self._name = self._curseforgeData["name"]
        self._ID = self._curseforgeData["id"]
        self._versions = callCurseForge.sortVersionList(self._curseforgeData)
    
class ModProfile(object):
    modList:list[Mod]
    priorityList:list[ModPriority]
    selectedVersion:str
    name:str
    
    def __init__(self, modList:list[Mod] = [],
                 priorityList:list[ModPriority] = [
                     ModPriority("High Priority", 255, 85, 0),
                     ModPriority("Low Priority", 255, 255, 0)],
                 selectedVersion:str = "1.21.5",
                 name = "New Profile"):
        # assign variables
        self.modList = modList
        self.priorityList = priorityList
        self.selectedVersion = selectedVersion
        self.name = name

    def __str__(self):
        output = f"{self.name}:\n"

        if self.modList:
            for mod in self.modList:
                output += mod.__str__() + "\n"
        else:
            output += "No mods in profile"

        return output[:-1]

    # Returns a float that represents how many of the mods in this profile are ready for the selected version, in percentage terms.
    def getPercentReady(self):
        readyMods = 0
        
        for mod in self.modList:
            if self.selectedVersion in mod.getVersionList():
                readyMods += 1
        
        if (len(self.modList) == 0):
            return 0
        else:
            return (readyMods/len(self.modList)) * 100

    # Returns profile information as a dictionary  
    def createDict(self):
        modlist = []
        for mod in self.modList:
            modlist.append(mod.createDict())
        return {
            "name":self.name,
            "version":self.selectedVersion,
            "modlist":modlist
        }
