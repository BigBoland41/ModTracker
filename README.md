# Mod Tracker

Make downloading and keeping track of all your mods easy and seamless!

Mod tracker is a windows app that keeps track of the mods you're waiting on to update to the latest Minecraft version. It also lets you download all them with a single click, easily share them with your friends, and more! Say goodbye to that mile long bookmark folder of Mondrinth and CurseForge links - Mod Tracker will do the job for you!

- Create profile(s) - a list of Minecraft mods you want track. Either Modrinth or CurseForge will work!
- Easily see what mods are updated by looking at the color-coded list or detailed pie chart.
- **New!** Download all your mods with a single click!
- **New!** Share your mods easily by exporting your profile.
- Assign priority levels to categorize your must-have mods your nice-to-have mods. (This is reflected in the pie chart!)

**[Download here!](https://github.com/Stephen-Nuttall/ModTracker/releases)**
[Click here for instructions](#how-to-download)

![alt text](screenshot%201.png)

*Please note that this app is still in beta, so expect some bugs. If you encounter a bug or have ideas to improve Mod Tracker, create an issue on our [issues page](https://github.com/Stephen-Nuttall/ModTracker/issues).*


## How to Download
1. Go to our [releases page](https://github.com/Stephen-Nuttall/ModTracker/releases).
2. Open the assets dropdown on the latest release, and download the installer.
3. Run the installer, and you should be good!

Alternatively, you can install the executable directly from the latest action on our [actions page](https://github.com/Stephen-Nuttall/ModTracker/actions/workflows/build-test.yml). Note that there is currently a bug where the unittest results will be blank.


## Changes in Beta 4.0
- **Import a profile based on your mods folder!** A new option when creating a profile has been added: import from mods folder. This option will look through a given folder (mods folder by default) and download mods based on the information inside the jar files. Unfortunately, this isn't guaranteed to find the correct mods, so be sure to double check the profile after creating it!
- **Reorganize mods in the table** by drag and dropping the rows! Either drag a row in between two other rows to insert it, or drag a row directly on top another row to swap the two.
- Mod Tracker no longer crashes when Modrinth or CurseForge APIs cannot be reached. Instead, a warning is shown and Mod Tracker proceeds with its saved data. Please note that "offline mode" is still not properly supported and some features may not work as intended.
- Using a new CurseForge API key.
- Bugfixes and refactoring.

If there are any issues with this version Mod Tracker, report it on our [issues page](https://github.com/Stephen-Nuttall/ModTracker/issues).

## Technical Details
For those who want to download this repository on your own computer, here's some helpful information.

To run Mod Tracker in your IDE:
- Install Python 3, then install the PyQt6, PyQt6-Charts, requests, and levenshtein libraries using pip.
- Create a file called API_Keys.py and create a variable inside it called CurseForge. Set it to your API key for CurseForge. Do not use our API key for your project.
- Run the main.py file.

To generate your own executable:
- Install the pyinstaller library (make sure you also have other libraries installed).
- Run `pyinstaller --name "Mod Tracker" --onefile --noconsole --icon=icon.ico main.py --add-data "fonts/fontello.ttf;fonts"`.
- The executable can then be found in the newly generated dist directory.

To generate your own installer:
- Download [Inno Setup](https://jrsoftware.org/isinfo.php).
- Run inno setup script.iss with Inno Setup. Make sure you've already built the executable.

To run unit tests, run the tests.py file. You can also test specific modules using a file with the test_ prefix, found in the tests directory.

<sup> README updated 10/1/2025 (unless I forgot to update this)