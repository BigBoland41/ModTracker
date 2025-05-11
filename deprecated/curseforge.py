# ---------- DEPRECATED  ----------
# Was used for testing stuff. NOT part of build

# Add the parent directory to the Python path
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import mod, json

testMod = mod.Mod(url="https://www.curseforge.com/minecraft/worlds/iris")
mod_slug = testMod._url.rstrip("/").split("/")[-1]
testMod._callCurseForgeAPI(mod_slug)

with open(f"deprecated/curseforge.json", "w") as file:
    json.dump(testMod._curseforgeData, file, indent=4)

testMod._extractCurseforge()
print(f"{testMod.getName()} versions: {testMod.getVersionList()}")