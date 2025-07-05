import requests, re

_curseforgeRegex = r"^https:\/\/(www\.)?curseforge\.com\/minecraft\/mc-mods\/[a-zA-Z0-9-_]+\/?$"
_requestTimeout = 10.0 # How many seconds to wait for an API call before timeout.

# Verify if the URL this mod was initialized with is specifically a Curseforge URL
def verifyURL(url:str):
    curseforge = re.compile(_curseforgeRegex)
    return curseforge.match(url)

def modData(mod_slug):
    apiKey = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"
    gameID = 432 # 432 = Minecraft

    headers = {"Accept": "application/json", "x-api-key": apiKey}
    url = f"https://api.curseforge.com/v1/mods/search?gameId=432&slug={mod_slug}"

    try:
        response = requests.get(url, headers=headers, timeout=_requestTimeout)
    except requests.exceptions.Timeout:
        print(f"Curseforge API request timed out after {_requestTimeout} seconds")

    if response.status_code == 200:
        try:
            # take the first search result that is not a custom map or texture pack
            for entry in response.json()["data"]:
                if entry["primaryCategoryId"] != 4475 and entry["primaryCategoryId"] != 4464:
                    return entry
        except IndexError:
            return False
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return False