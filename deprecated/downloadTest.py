# Add the parent directory to the Python path
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# import requests, webbrowser

# def helper(url:str):
#     response = requests.get(url)

#     if response.status_code == 200:
#         return response.json()  
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return False

# modJson = helper("https://api.modrinth.com/v2/project/sodium/version")
# versionJson = helper(f"https://api.modrinth.com/v2/version/{modJson[1]["id"]}")
# webbrowser.open(versionJson["files"][0]["url"])

import mod
testMod = mod.Mod(url="https://modrinth.com/mod/ferrite-core")
testMod.downloadMod("Fabric")