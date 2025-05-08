import mod
import json

# Convert json data for a mod into a mod object
def _dictToMod(data):
        priorityData = data["priority"]

        priorityLevel = mod.ModPriority(priorityData["name"], red=priorityData["r"], green=priorityData["g"], blue=priorityData["b"])
        return mod.Mod(modName=data["name"], modPriority=priorityLevel, modVersions=data["versions"], url=data["url"], modID=data["id"])

# Convert json data for a mod profile into a mod profile object
def _dictToModProfile(data):
    newModList = []
    modListData = data["modlist"]
    for newMod in modListData:
        newModList.append(_dictToMod(newMod))
    return mod.ModProfile(modList = newModList, name=data["name"], selectedVersion=data["version"])
    
# --- Deprecated ---
# Open a json file, read the data, and create a single list of mods (rather than a list of mod profiles)
def _createModList(filename="mods.json"):
        newModList = []
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for entry in data:
                    newModList.append(_dictToMod(entry))
        except FileNotFoundError:
            return []
        return newModList

# Open a json file, read the data, and create a list of mod profiles from it
def createProfileList(filename="mods.json"):
    newProfileList = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for entry in data:
                newProfileList.append(_dictToModProfile(entry))
    except FileNotFoundError:
        return []
    return newProfileList