import requests

CFKEY = "$2a$10$QIDeQbKDRhOQZgmcVHKxYeTSI/RlHH8oOzRnPhd6Rb4Dcj2l3k27a"

URL = "https://api.curseforge.com/v1/"

ID = 432 #game ID for minecraft

headers = {
    "X-Api-Key": CFKEY
}

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
