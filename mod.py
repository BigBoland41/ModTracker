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
    name:str
    url:str
    ID:int
    versions:list[str]
    modrinth:dict
    curseforge:dict
    
    # can pass mod info directly for testing, but can also just call constructor with a url and it will get all 
    # relevant info from the api and store it all
    def __init__(self, modName = "Untitled Mod", modID = -1, modVersions = ["No versions found"],
                 modPriority = ModPriority(), fromModrinth = False, fromCurseforge = False, url = -1):
        self.name = modName
        self.ID = modID
        self.url = url
        self.versions = modVersions
        self.priority = modPriority
        self.modrinth = fromModrinth
        self.curseforge = fromCurseforge

        if(url != -1):
            self.refreshMod()

    def __str__(self):
        return f"{self.name} version: {self.getCurrentVersion()}, priority: {self.priority}"


    def getName(self):
        return self.name
    
    def getID(self):
        return self.ID

    def getCurrentVersion(self):
        return self.versions[-1]
    
    def getVersionList(self):
        return self.versions
    
    def getURL(self):
        return self.url

    def _getCurrentVersion(self):
        pass

    def _getVersions(self):
        pass
    
    def _getModID(self):
        pass

    def getData(self):
        apiKey = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"
        # modrinth data
        mod_slug = self.url.rstrip("/").split("/")[-1]
        url = f"https://api.modrinth.com/v2/project/{mod_slug}"
        response = requests.get(url)
        
        if response.status_code == 200:
            self.modrinth = response.json()  
        else:
            print(f"Error: {response.status_code}, {response.text}")

        # curseforge data
        headers = {"x-api-key": apiKey}
        params = {"gameId": 432, "searchFilter": mod_slug}  # 432 = Minecraft
        response = requests.get(f"https://api.curseforge.com/v1/mods/search", headers=headers, params=params)
        if(response.status_code == 200):
            modList = response.json().get("data", [])
            for mod in modList:
                print(mod["slug"])
                if mod["slug"] == mod_slug:
                   self.curseforge = mod
        else: 
            print(f"Error: {response.status_code}, {response.text}")

    
    def extractModrinth(self):
        if (self.modrinth == -1):
            return -1
        self.name = self.modrinth["title"]
        self.ID = self.modrinth["id"]
        self.versions = self.modrinth["game_versions"]

    def refreshMod(self):
        self.getData()
        self.extractModrinth()



