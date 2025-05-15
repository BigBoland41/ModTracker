# Mod Tracker

Mod tracker is an app that helps you keep track of the mods you've been so patiently waiting on updating to the newest Minecraft version. Say goodbye to that mile long bookmark folder of Mondrinth and CurseForge links - Mod Tracker will do the job for you!

**[Click here for download instructions](#how-to-download)**

*Please note that this app is still in beta, so expect some bugs. If you encounter a bug, or have ideas on how to improve Mod Tracker, create an issue on our [issues page](https://github.com/BigBoland41/ModTracker/issues).*

![alt text](screenshot%201.png)

## How to Download
1. Go to our [releases page](https://github.com/BigBoland41/ModTracker/releases).
2. Open the assets dropdown on the latest release, and download the installer.

Alternatively, you can install the executable directly from the latest action on our [actions page](https://github.com/BigBoland41/ModTracker/actions/workflows/build-test.yml). Note that there is currently a bug where the unittest results will be blank.


## Changes in Beta 2.0
- **Proper Curseforge support!** While it was technically supported it in our MVP, we actually used the Mondrinth data instead, and didn't support mods only found on Curseforge.
- **Massive improvement in loading times** achieved by putting each mod's API call on a separate thread.
- **New loading window** that displays when the app is launching. In the future we want it to be animated, but for now it's just a still image.
- **Added an app icon** created by us - a Minecraft monkey wrench!
- Error text will now appear when the user attempts to add a mod with an invalid URL.
- The user can now give a mod a custom priority level that was created in another profile.
- Data is saved to file more often.
- Bugfixes and refactoring.

If there are any issues with this version Mod Tracker, report it on our [issues page](https://github.com/BigBoland41/ModTracker/issues).

## Project Details

### Motivation and Objective

A large portion of the Minecraft player base installs mods for their game. However, mods only support specific versions of Minecraft, so when a update is released, mods become outdated and need to be updated manually by their developer. When using lots mods, it can be difficult to keep track of which mods support which versions, and which are ready for the next update. People often did this by just going down a list of links from Modrinth and Curseforge, manually checking each mod's version.

Our goal is to make the experience of keeping track of all your mods easy and seemless.

ModTracker is a desktop application designed to simplify the task of tracking supported game versions for Minecraft mods. Users can create profiles containing a list of selected Minecraft mods to track. The profile will display information based on the Minecraft version the user wishes to target. Each mod in a profile will have a priority level indicating the importance of that mod to be supported by the selected Minecraft version. Using the assigned priority levels and the supported versions of each mod, ModTracker will graph the proportion of supported and unsupported mods for the selected game version.

### How to Run Our Project

To run Mod Tracker in your IDE:
- Install Python 3, then install the PyQt6, requests, and PyQt6-Charts libraries using pip.
- Run the main.py file.

To generate your own executable:
- Install the pyinstaller library (make sure you also have other libraries installed).
- Run `pyinstaller --name "Mod Tracker" --onefile --noconsole --icon=icon.ico main.py`.
- The executable can then be found in the newly generated dist directory.

To generate your own installer:
- Download [Inno Setup](https://jrsoftware.org/isinfo.php).
- Run inno setup script.iss with Inno Setup. Make sure you've already built the executable.

To run unit tests, run the tests.py file. You can also test specific modules using a file with the test_ prefix, found in the tests directory.

<sup> README updated 5/15/2025