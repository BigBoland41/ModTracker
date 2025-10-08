from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys, os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import Backend.mod as mod, Backend.loadFromJson as loadFromJson

profileManager:mod.ProfileManager

async def lifespan(app: FastAPI):
    global profileManager
    profileManager = mod.ProfileManager([mod.Profile([
        mod.Mod(url="https://modrinth.com/mod/sodium"),
        mod.Mod(url="https://modrinth.com/mod/lithium")])], [
        mod.Priority("High Priority"), mod.Priority("Medium Priority"), mod.Priority("Low Priority")
    ])

    yield

    profileManager._profileList.clear()
    profileManager._priorityList.clear()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get-data")
async def getData():
    global profileManager
    if profileManager:
        return profileManager.createDict()
    else:
        return {"errorMessage" : "ERROR: profileManager does not exist!"}

@app.post("/get-profile-list")
async def getProfileList():
    global profileManager
    profileData = profileManager.createDict()
    return profileData["profileList"]

@app.post("/get-priority-list")
async def getPriorityList():
    global profileManager
    profileData = profileManager.createDict()
    return profileData["priorityList"]

@app.post("/get-profile")
async def getProfile(request: Request):
    global profileManager
    data = await request.json()
    profileIndex = data.get("profileIndex", 0)

    profile = profileManager.getProfile(profileIndex)
    
    if profile:
        return {
            "profile": profile.createDict(),
            "modListLength" : len(profile.modList),
            "errorMessage" : "None"
        }
    else:
        return {
            "errorMessage" : f"Could not find a profile at index {profileIndex}." 
        }
    
@app.post("/load-profiles")
async def loadProfiles():
    global profileManager
    profileList = loadFromJson.createProfileList()
    for profile in profileList:
        profileManager.addProfile(profile)   

    return profileManager.createDict()     

@app.post("/add-mod")
async def addMod(request: Request):
    global profileManager
    try:
        data = await request.json()
        url = data.get("url", "Something went wrong")
        profileIndex = data.get("profileIndex", 0)

        profile:mod.Profile = profileManager.getProfile(profileIndex)
        
        if profile.addMod(url):
            return {"errorMessage" : "None"}
        else:
            return {"errorMessage" : "Unable to add this mod. Check the URL you provided and verify it's correct."}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return { "errorMessage" : f"{str(e)}.\nException Details: {exc_type} {fname} {exc_tb.tb_lineno}"}
    
@app.post("/test_func")
async def test_func(request: Request):
    data = await request.json()
    url = data.get("url", "Something went wrong")
    modObj = mod.Mod(url=url)
    
    return modObj.createDict()