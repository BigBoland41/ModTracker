import mod, json, threading

# Convert json data for a mod into a mod object
def _dictToMod(data):
    priorityData = data["priority"]
    priorityLevel = mod.ModPriority(priorityData["name"], red=priorityData["r"], green=priorityData["g"], blue=priorityData["b"])

    if "tablePosition" in data:
        tablePos = data["tablePosition"]
    else:
        tablePos = -1
        
    modObj = mod.Mod(modName=data["name"], modPriority=priorityLevel, modVersions=data["versions"], url=data["url"], modID=data["id"], tablePosition=tablePos)
    return modObj

# Convert json data for a mod profile into a mod profile object. Create each mod object on its own thread, as each will make an API call.
def _dictToModProfile(data):
    threadList = []
    
    newModList = []
    modListData = data["modlist"]

    def threadHelper(newMod, list):
        modObj = _dictToMod(newMod)

        if modObj.isValid():
            list.append(modObj)

    for newMod in modListData:
        thread = threading.Thread(target=threadHelper, args=(newMod, newModList))
        threadList.append(thread)
        thread.start()

    for thread in threadList:
        thread.join()

    return mod.ModProfile(modList = newModList, name=data["name"], selectedVersion=data["version"])
    
# ----- Deprecated -----
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