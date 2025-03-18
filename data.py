import requests

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


def search_mod(modName, gameID):
    url = f"{URL}mods/search"
    params = {"gameId": gameID, "searchFilter": modName}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        mods = response.json().get("data", [])  # Extracts the 'data' list
        
        # Extract only Mod Name and Mod ID
        results = [(mod["id"], mod["name"]) for mod in mods]
        return results
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    
def mod_info(modID):
    url = f"{url}mods/{modID}"



if __name__ == "__main__":
    results = search_mod("weed", ID)
    if(results != None):
        for id, name in results:
            print(f"Mod ID: {id} - name: {name}")
    else:
        print("got noting")