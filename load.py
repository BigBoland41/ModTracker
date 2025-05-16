import mod, json, threading, os

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

# Open a json file, read the data, and create a list of mod profiles from it
def createProfileList(filename="mods.json"):
    appdata = os.getenv('APPDATA')
    directory = os.path.join(appdata, 'ModTracker')
    os.makedirs(directory, exist_ok=True)
    json_path = os.path.join(directory, filename)

    newProfileList = []
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            for entry in data:
                newProfileList.append(_dictToModProfile(entry))
    except FileNotFoundError:
        return []
    return newProfileList