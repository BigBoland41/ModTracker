# Mod Tracker

Mod tracker is an app that helps you keep track of the mods you've been so patiently waiting on updating to the newest Minecraft version. Say goodbye to that mile long bookmark folder of Mondrinth and CurseForge links - Mod Tracker will do the job for you!

# How To Run

To run application, either...
- Run dist/detailsWindow/detailsWindow.exe
OR
- Install Python 3, then install the PyQt6, requests, and PyQt6-Charts libraries using pip install PyQt6 and pip install requests.
- Run the detailsWindow.py file.

Generate an executable by:
- Install the pyinstaller library (make sure you also have other libraries installed)
- Run pyinstaller detailsWindow.py
- The executable can then be found in the newly generated dist/detailsWindow directory

To run unit tests, run the tests.py file.

# Project Details

## Motivation and Objective

A large portion of the Minecraft player base installs mods for their game. However, while the community is large, it can be disorganized. Minecraft mods only support specific versions of the game. When a Minecraft update is released, mods become outdated and need to be updated manually by their developer. When installing multiple mods, it can be difficult to keep track of which mods support which versions. While Minecraft mod repositories exist and display the latest version a mod supports, they do not include a simple way to create a list of mods and show the version they all support.

Our goal is to make the experience of keeping track of all your mods easy and seemless.

ModTracker is a desktop application designed to simplify the task of tracking supported game versions for Minecraft mods. Users can create profiles containing a list of selected Minecraft mods to track. The profile will display information based on the Minecraft version the user wishes to target. Each mod in a profile will have a priority level indicating the importance of that mod to be supported by the selected Minecraft version. Using the assigned priority levels and the supported versions of each mod, ModTracker will graph the proportion of supported and unsupported mods for the selected game version.

## Architecture

After opening the app, the user can select a mod profile, which contains a list of mods, or create a new one. The user can then add mods to the profile they want tracked, change the priority level of specific mods, etc. When new information is needed, an API call will be made to get information about all mods.

[Sequence Diagram](https://cdn.discordapp.com/attachments/1336782574403457146/1344455646971695147/Screenshot_2025-02-26_at_6.44.06_PM.png?ex=67db5765&is=67da05e5&hm=f9e517b43c078790626319905b22c6b301c17585f6d148311ffe68b9ffa865e1&)

To accomplish this, we're utilizing several technologies:
- PyQt6 - A cross-platform GUI framework for building applications in python
- JSON library for API calls
- Python unittest library for testing



There's still a lot of work to be done, but our team is hard at work. We hope to release Mod Tracker some time in the near future!
<sup> README updated 3/18/2025