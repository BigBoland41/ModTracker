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
    _modrinthData:dict
    _curseforgeData:dict
    
    # can pass mod info directly for testing, but can also just call constructor with a url and it will get all 
    # relevant info from the api and store it all
    def __init__(self, modName = "Untitled Mod", modID = -1, modVersions = ["No versions found"],
                 modPriority = ModPriority(), fromModrinth = False, fromCurseforge = False, url = -1):
        self.priority = modPriority
        self._name = modName
        self._ID = modID
        self._url = url
        self._versions = modVersions
        self._modrinthData = fromModrinth
        self._curseforgeData = fromCurseforge

        if(url != -1):
            self.refreshMod()

    def __str__(self):
        return f"{self._name} version: {self.getCurrentVersion()}, priority: {self.priority}"

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
    
    def verifyURL(self):
        curseforge = re.compile(r"^https:\/\/(www\.)?curseforge\.com\/minecraft\/mc-mods\/[a-zA-Z0-9-_]+\/?$")
        modrinth = re.compile(r"^https:\/\/(www\.)?modrinth\.com\/mod\/[a-zA-Z0-9-_]+\/?$")
        return modrinth.match(self._url) or curseforge.match(self._url)

    def getData(self):
        if(not self.verifyURL()):
            # print("no valid url")
            return
        apiKey = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"
        # modrinth data
        mod_slug = self._url.rstrip("/").split("/")[-1]
        url = f"https://api.modrinth.com/v2/project/{mod_slug}"
        response = requests.get(url)
        
        if response.status_code == 200:
            self._modrinthData = response.json()  
        else:
            print(f"Error: {response.status_code}, {response.text}")

        # curseforge data
        headers = {"x-api-key": apiKey}
        params = {"gameId": 432, "searchFilter": mod_slug}  # 432 = Minecraft
        response = requests.get(f"https://api.curseforge.com/v1/mods/search", headers=headers, params=params)
        if(response.status_code == 200):
            modList = response.json().get("data", [])
            for mod in modList:
                # print(mod["slug"])
                if mod["slug"] == mod_slug:
                   self._curseforgeData = mod
        else: 
            print(f"Error: {response.status_code}, {response.text}")

    
    def extractModrinth(self):
        if (self._modrinthData == False):
            return -1
        self._name = self._modrinthData["title"]
        self._ID = self._modrinthData["id"]
        self._versions = self._modrinthData["game_versions"]

    def refreshMod(self):
        self.getData()
        self.extractModrinth()

    def createDict(self):
        return {
            "priorityname" : self.priority.name,
            "priorityr" : self.priority.r,
            "priorityg" : self.priority.g,
            "priorityb" : self.priority.b,
            "name" : self._name,
            "id" : self._ID,
            "url" : self._url,
            "versions" : self._versions,
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

    def showDetailsWindow(self, window):
        from windows import DetailsWindow
        self._profileView = DetailsWindow(window, self.modList, self.priorityList, self.selectedVersion)

    def getPercentReady(self):
        readyMods = 0
        
        for mod in self.modList:
            if self.selectedVersion in mod.getVersionList():
                readyMods += 1
        
        if (len(self.modList) == 0):
            return 0
        else:
            return (readyMods/len(self.modList)) * 100
