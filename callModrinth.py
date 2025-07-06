import requests, re

_modrinthRegex = r"^https:\/\/(www\.)?modrinth\.com\/mod\/[a-zA-Z0-9-_]+\/?$"
_requestTimeout = 10.0 # How many seconds to wait for an API call before timeout.


# Verify if the URL this mod was initialized with is specifically a Modrinth URL
def verifyURL(url:str):
    modrinth = re.compile(_modrinthRegex)
    return modrinth.match(url)

def _genericModrinthCall(url:str):
    try:
        response = requests.get(url, timeout=(_requestTimeout, _requestTimeout))
    except requests.exceptions.Timeout:
        print(f"Mondrinth API request timed out after {_requestTimeout} seconds")
    
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return False

def modData(mod_slug:str):
    url = f"https://api.modrinth.com/v2/project/{mod_slug}"
    return _genericModrinthCall(url)

def modVersionList(mod_slug:str):
    url = f"https://api.modrinth.com/v2/project/{mod_slug}/version"
    return _genericModrinthCall(url)

def downloadMod(mod_slug:str, loader:str, version:str):
    loader = loader.lower()
    versionList = modVersionList(mod_slug)

    for ver in versionList:
        if loader in ver["loaders"] and version in ver["game_versions"]:
            for file in ver["files"]:
                return file["url"]
            
    return False