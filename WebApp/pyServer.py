from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys, os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import Backend.mod as mod

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run-test")
async def run_test(request: Request):
    data = await request.json()
    url = data.get("url", "Something went wrong")
    modObj = mod.Mod(url=url)
    
    return {
        "name": modObj.getName(),
        "version": modObj.getCurrentVersion(),
        "priority": modObj.priority.name,
        "tablePosition": modObj.getTablePosition()
    }
