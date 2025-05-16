# ---------- DEPRECATED  ----------
# Was used for testing stuff. NOT part of build

import requests
import json
import re

CFKEY = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"

URL = "https://api.curseforge.com/v1/"

ID = 432 #game ID for minecraft

headers = {
    "X-Api-Key": CFKEY
}

# just here to test the api call
def test(): 
    response = requests.get(URL + "games", headers=headers)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)  # This helps see if CurseForge returned anything

    if response.status_code == 200:
        try:
            data = response.json()
            print(data)
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is empty or not JSON format.")
    else:
        print(f"Error {response.status_code}: {response.reason}")


def search_mod(modName):
    url = f"{URL}mods/search"
    params = {"gameId": ID, "searchFilter": modName}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        mods = response.json().get("data", [])  # Extracts the 'data' list
        
        # Extract only Mod Name and Mod ID
        results = [(mod["id"], mod["name"]) for mod in mods]
        return results
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def mod_lookup(url):
    
    match = re.search(r"mc-mods/([^/]+)", url)
    if not match:
        print("Invalid CurseForge mod URL.")
        return None

    mod_slug = match.group(1)  # Get the mod's slug (URL-friendly name

    lookupUrl = f"{URL}mods/search"
    params = {"gameId": ID, "searchFilter": mod_slug, "pages": 4000}
    pageNumber = 1
    while(pageNumber <= 25):
        response = requests.get(lookupUrl, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            return None

        mods = response.json().get("data", [])
        
        mod_info = next((mod for mod in mods if mod['links']['websiteUrl'] == url), None)
        
        if mod_info:
            print(mod_info['links']['websiteUrl'])
            return mod_info['id']  
        pageNumber += 1

def mod_info(modID):
    url = f"{URL}mods/{modID}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"API Error {response.status_code}: {response.text}")
        return None

    mod = response.json().get("data", [])
    with open("mod_info.json", "w") as json_file:
        json.dump(mod, json_file, indent=4)
    #print(mod)
    latestFiles = mod['latestFiles']
    d = latestFiles[-1] 
    print(f"Mod name: {mod['name']}, Mod Version: {d['sortableGameVersions'][-1]['gameVersion']}")



if __name__ == "__main__":
    results = search_mod("worldedit")
    if(results != None):
        for id, name in results:
            print(f"Mod ID: {id} - name: {name}")
    else:
        print("got noting")

    print(mod_lookup("https://www.curseforge.com/minecraft/mc-mods/worldedit"))
    mod_info(225608)