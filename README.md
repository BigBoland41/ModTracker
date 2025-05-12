# Mod Tracker

Mod tracker is an app that helps you keep track of the mods you've been so patiently waiting on updating to the newest Minecraft version. Say goodbye to that mile long bookmark folder of Mondrinth and CurseForge links - Mod Tracker will do the job for you!

## How to Download

To download and run Mod Tracker:
- Open your browser and go to our [GitHub Actions page](https://github.com/BigBoland41/ModTracker/actions/workflows/build-test.yml).
- You can now see a log of all attempted builds, which automatically run after committing to the main branch. Click the most recent one.
- Download build-executable.zip from the artifacts.
You can optionally download the automatic test results in unittest-results.zip. Note that there is currently a bug where the unittest results will be blank.

## Changes in Beta 2.0
- **Proper Curseforge support!** While it was technically supported it in our MVP, we actually used the Mondrinth data instead, and didn't support mods only found on Curseforge.
- **Massive improvement in loading times** achieved by putting each mod's API call on a separate thread.
- **New loading window** that displays when the app is launching. In the future we want it to be animated, but for now it's just a still image.
- Error text will now appear when the user attempts to add a mod with an invalid URL.
- The user can now give a mod a custom priority level, even if it was created in another profile.
- Data is saved to file more often.
- Bugfixes and refactoring.

If there are any issues with this version Mod Tracker, or you have ideas on how to improve the user experience, please post an issue on our [issue tracker](https://github.com/BigBoland41/ModTracker/issues).

![Screenshot](https://media.discordapp.net/attachments/1279545631622299680/1371555996832370729/image.png?ex=6823908f&is=68223f0f&hm=1d20fbe2de4e46522b8896018b1172baba9dcd9f734e3e3bdd8b97f16b2f9e9d&=&format=webp&quality=lossless&width=1593&height=856)

## Project Details

### Motivation and Objective

A large portion of the Minecraft player base installs mods for their game. However, mods only support specific versions of Minecraft, so when a update is released, mods become outdated and need to be updated manually by their developer. When using lots mods, it can be difficult to keep track of which mods support which versions, and which are ready for the next update. People often did this by just going down a list of links from Modrinth and Curseforge, manually checking each mod's version.

Our goal is to make the experience of keeping track of all your mods easy and seemless.

ModTracker is a desktop application designed to simplify the task of tracking supported game versions for Minecraft mods. Users can create profiles containing a list of selected Minecraft mods to track. The profile will display information based on the Minecraft version the user wishes to target. Each mod in a profile will have a priority level indicating the importance of that mod to be supported by the selected Minecraft version. Using the assigned priority levels and the supported versions of each mod, ModTracker will graph the proportion of supported and unsupported mods for the selected game version.

### How to Run Our Project

To run Mod Tracker in your IDE:
- Install Python 3, then install the PyQt6, requests, and PyQt6-Charts libraries using pip install PyQt6 and pip install requests.
- Run the main.py file.

To generate your own executable:
- Install the pyinstaller library (make sure you also have other libraries installed)
- Run pyinstaller --name ModTracker --onefile --noconsole main.py
- The executable can then be found in the newly generated dist directory

To run unit tests, run the tests.py file. You can also test specific modules using a file with the test_ prefix.

<sup> README updated 5/12/2025