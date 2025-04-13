from PyQt6 import QtGui
import requests
import re
class ModPriority(object):
    name:str
    color:QtGui.QColor

    def __init__(self, newName = "New Priority Level", red = 255, green = 255, blue = 255, color:QtGui.QColor = None):
        self.name = newName
        if color == None:
            self.color = QtGui.QColor(red, green, blue)
        else:
            self.color = color

    def __str__(self):
        return f"{self.name}"

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
            print("no valid url")
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



