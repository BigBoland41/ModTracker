import mod
import json



def dictToMod(data):
        prioData = data["priority"]

        prio = mod.ModPriority(prioData["name"], red=prioData["r"], green=prioData["g"], blue=prioData["b"])
        return mod.Mod(modName=data["name"], modPriority=prio, modVersions=data["versions"], url=data["url"], modID=data["id"])

def dictToModProfile(data):
    newModList = []
    modListData = data["modlist"]
    for newMod in modListData:
        newModList.append(dictToMod(newMod))
    return mod.ModProfile(modList = newModList, name=data["name"], selectedVersion=data["version"])
    
    

def createModList(filename="mods.json"):
        newModList = []
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for entry in data:
                    newModList.append(dictToMod(entry))
        except FileNotFoundError:
            return []
        return newModList

def createProfileList(filename="mods.json"):
    newProfileList = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for entry in data:
                newProfileList.append(dictToModProfile(entry))
    except FileNotFoundError:
        return []
    return newProfileList