# ModTracker
1	Project Overview

1.1	Motivation

Many dedicated Minecraft players install a wide variety of mods to their game to improve their experience. These mods are almost always maintained by independent solo developers in their free time, so when a new Minecraft version is released, they all update to support it at very different and unpredictable rates. While waiting, the primary way of keeping track of all these mods is by manually visiting the download site for each mod regularly to see if it’s been updated. This task is tedious and difficult to keep track of.
We want to create a desktop application that would keep track of all these mods for you. By simply adding each mod’s download link to a list, the software will use the APIs of the most popular download sites to check if new versions have been released or not. Instead of manually going down a list of download links, the user can open the software and it will check automatically, greatly simplifying the process. The user would also have access to additional features that will be discussed later in this proposal, including various organization options and a pie chart displaying visually how many of their mods are ready for the newest Minecraft version.

There are currently no good alternatives to the role that Mod Tracker will fill. While the two major download sites for Minecraft mods - CurseForge and Modrinth - both have a system allowing the user to view a list of all mods they “follow,” neither show the latest Minecraft version in directly in that view, and will only allow the user to follow mods from their site. No other pre-existing solution in the Minecraft space has a feature allowing the user to view a custom list of mods and their supported versions of Minecraft at a glance, and certainly not the organization options and charts that our software will offer. Mod Tracker will fill a unique role that has no alternatives in the Minecraft space.

1.2	Objectives

The main objective of Mod Tracker is to easily track which of their mods are available for a given version of Minecraft. Mod Tracker will allow the user to add a supported download site for a mod to a list of mods called a profile. The user can then view that profile and see all the mods they’ve added to that list, as well as the latest versions of Minecraft they’re compatible with. Each mod should also have a customizable priority level the user can set, which will be displayed if the mod is not available for the selected version of Minecraft. A pie chart will also be displayed, to show visually how many mods are ready for the selected version. The proposed UI for the profile view follows the spreadsheet displayed in figure 1.

