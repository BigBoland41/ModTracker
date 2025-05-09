from PyQt6 import QtGui
import requests, re

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
    
    # can pass mod info directly for testing, but can also just call constructor with a url and it will get all 
    # relevant info from the api and store it all
    def __init__(self, modName = "Untitled Mod", modID = -1, modVersions = ["No versions found"],
                 modPriority = ModPriority(), url = -1, tablePosition = -1):
        self.priority = modPriority
        self._name = modName
        self._ID = modID
        self._url = url
        self._versions = modVersions
        self._tablePosition = tablePosition

        self._modrinthData = False
        self._curseforgeData = False

        if(url != -1):
            self.refreshMod()

    def __str__(self):
        return f"{self._name} version: {self.getCurrentVersion()}, priority: {self.priority}"
    
    def __lt__(self, other):
        return self._tablePosition < other._tablePosition

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
        return self._url

    def getVersions(self):
        return self._versions
    
    def getModrinthData(self):
        return self._modrinthData
    
    def getCurseforgeData(self):
        return self._curseforgeData
    
    def isValid(self):
        return self._modrinthData != False or self._curseforgeData != False
    
    # Verify if the URL this mod was initialized with is valid
    def verifyURL(self):
        curseforge = re.compile(self._curseforgeRegex)
        modrinth = re.compile(self._modrinthRegex)
        return modrinth.match(self._url) or curseforge.match(self._url)

    # Runs when the mod's data needs to be reset. Makes an API call and extracts the raw data
    def refreshMod(self):
        print(".", end="")
        self.callAPIs()
        self.extractModrinth()

    # Use the URL this mod was initialized with to get its data from CurseForge and Modrinth
    def callAPIs(self):
        if(not self.verifyURL()):
            return

        mod_slug = self._url.rstrip("/").split("/")[-1]
        
        self.callMondrinthAPI(mod_slug)
        self.callCurseForgeAPI(mod_slug)

    def callMondrinthAPI(self, mod_slug):
        url = f"https://api.modrinth.com/v2/project/{mod_slug}"
        response = requests.get(url)
        
        if response.status_code == 200:
            self._modrinthData = response.json()  
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def callCurseForgeAPI(self, mod_slug):
        apiKey = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"
        gameID = 432 # 432 = Minecraft

        headers = {"x-api-key": apiKey}
        params = {"gameId": gameID, "searchFilter": mod_slug}
        response = requests.get(f"https://api.curseforge.com/v1/mods/search", headers=headers, params=params)

        if response.status_code == 200:
            modList = response.json().get("data", [])
            for mod in modList:
                if mod["slug"] == mod_slug:
                   self._curseforgeData = mod
        else: 
            print(f"Error: {response.status_code}, {response.text}")

    # Extract modrinth json data from API call
    def extractModrinth(self):
        if (self._modrinthData == False):
            return -1
        
        self._name = self._modrinthData["title"]
        self._ID = self._modrinthData["id"]
        self._versions = self._modrinthData["game_versions"]

        if "tablePosition" in self._modrinthData:
            self._tablePosition = self._modrinthData["tablePosition"]

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
            "modlist":modlist,
            "version":self.selectedVersion,
            "name":self.name
        }
