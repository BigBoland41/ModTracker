import requests, re, json

_curseforgeRegex = r"^https:\/\/(www\.)?curseforge\.com\/minecraft\/mc-mods\/[a-zA-Z0-9-_]+\/?$"
_requestTimeout = 10.0 # How many seconds to wait for an API call before timeout.
_allowedCategoryIDs = [6, 4906, 6814, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441]

# Verify if the URL this mod was initialized with is specifically a Curseforge URL
def verifyURL(url:str):
    curseforge = re.compile(_curseforgeRegex)
    return curseforge.match(url)

def _genericCurseforgeCall(url:str):
    apiKey = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"
    # gameID = 432 # 432 = Minecraft

    headers = {"Accept": "application/json", "x-api-key": apiKey}

    try:
        response = requests.get(url, headers=headers, timeout=_requestTimeout)
    except requests.exceptions.Timeout:
        print(f"Curseforge API request timed out after {_requestTimeout} seconds")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return False

def modData(mod_slug):
    url = f"https://api.curseforge.com/v1/mods/search?gameId=432&slug={mod_slug}"
    json = _genericCurseforgeCall(url)

    try:
        # take the first search result that is not a custom map, texture pack, or anything that isn't a mod
        for entry in json["data"]:
            if entry["primaryCategoryId"] in _allowedCategoryIDs:
                return entry
        return False
    except IndexError:
        return False
    
def sortVersionList(curseforgeJson):
    fileIndexes = curseforgeJson["latestFilesIndexes"]
    parsedVersions = []

    for file in fileIndexes:
        parsedVersions.append(list(map(int, file["gameVersion"].split('.'))))

    sortedVersions = sorted(parsedVersions)

    unparsedVersions = []
    for versionComponents in sortedVersions:
        if len(versionComponents) == 3:
            versionStr = f"{versionComponents[0]}.{versionComponents[1]}.{versionComponents[2]}"
        else:
            versionStr = f"{versionComponents[0]}.{versionComponents[1]}"
        unparsedVersions.append(versionStr)
    
    return unparsedVersions

def modLoader_IDtoText(loaderID:int):
    match loaderID:
        case 0:
            return "Any"
        case 1:
            return "Forge"
        case 2:
            return "Cauldron"
        case 3:
            return "LiteLoader"
        case 4:
            return "Fabric"
        case 5:
            return "Quilt"
        case 6:
            return "NeoForge"
        case _:
            return -1

def downloadMod(curseforgeJson, mod_id:int, loader:str, version:str):
    fileIndexes = curseforgeJson["latestFilesIndexes"]

    # Get the FileId of the first file (from a sorted list) that has the right mod loader, and use it to get that file's download link
    for file in fileIndexes:
        # if file's gameVersion matches version, the file has a modLoader entry, and that modLoader entry matches loader, then make an API call for the download link
        if file["gameVersion"] == version and "modLoader" in file and (file["modLoader"] == 0 or modLoader_IDtoText(file["modLoader"]) == loader):
            url = f"https://api.curseforge.com/v1/mods/{mod_id}/files/{file["fileId"]}"
            downloadLink = _genericCurseforgeCall(url)["data"]["downloadUrl"]
            return downloadLink

    return False