# ---------- DEPRECATED  ----------
# Was used for testing stuff. NOT part of build

import requests
import json

def get_modrinth_mod_info(mod_slug):
    url = f"https://api.modrinth.com/v2/project/{mod_slug}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return f"Error: {response.status_code}, {response.text}"
    
if __name__ == "__main__":
    mod_info = get_modrinth_mod_info("sodium")
    with open("modrinth.json", "w") as json_file:
        json.dump(mod_info, json_file, indent=4)