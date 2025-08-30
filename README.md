# Mod Tracker

Make downloading and keeping track of all your mods easy and seemless!

Mod tracker is a windows app that keeps track of the mods you're waiting on to update to the latest Minecraft version. It also lets you download all them with a single click, easily share them with your friends, and more! Say goodbye to that mile long bookmark folder of Mondrinth and CurseForge links - Mod Tracker will do the job for you!

- Create profile(s) - a list of Minecraft mods you want track. Either Modrinth or CurseForge will work!
- Easily see what mods are updated by looking at the color-coded list or detailed pie chart.
- **New!** Download all your mods with a single click!
- **New!** Share your mods easily by exporting your profile.
- Assign priority levels to categorize your must-have mods your nice-to-have mods. (This is reflected in the pie chart!)

**[Download here!](https://github.com/BigBoland41/ModTracker/releases)**
[Click here for instructions](#how-to-download)

![alt text](screenshot%201.png)

*Please note that this app is still in beta, so expect some bugs. If you encounter a bug or have ideas to improve Mod Tracker, create an issue on our [issues page](https://github.com/BigBoland41/ModTracker/issues).*


## How to Download
1. Go to our [releases page](https://github.com/BigBoland41/ModTracker/releases).
2. Open the assets dropdown on the latest release, and download the installer.
3. Run the installer, and you should be good!

Alternatively, you can install the executable directly from the latest action on our [actions page](https://github.com/BigBoland41/ModTracker/actions/workflows/build-test.yml). Note that there is currently a bug where the unittest results will be blank.


## Changes in Beta 3.0 - Downloading and Exporting!
- **Download all your mods with one click!** A new "download all ready mods" button has been added to the profile details screen, along with a dropdown that lets you select the mod loader to use. Currently, the options are Forge, Fabric, Neoforge, and Quilt, but if there's demand for more, it shouldn't be too difficult to add!
- **Importing and exporting profiles!** Share your mod profile with a friend by clicking the new export button in the profile details screen. They can import it using the new import button in the profile select screen.
- Profiles can now be deleted from the profile select screen.
- Clicking on a mod's name from the mod list will open that mod's Modrinth or Curseforge page in your web browser.
- New pretty button icons have been added by importing Fontello - a font containing lots of commonly used icons. The license is included in the font folder.
- Bugfixes and refactoring.

If there are any issues with this version Mod Tracker, report it on our [issues page](https://github.com/BigBoland41/ModTracker/issues).

## Technical Details
For those who want to download this repository on your own computer, here's some helpful information.

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

<sup> README updated 8/30/2025 (unless I forgot to update this)