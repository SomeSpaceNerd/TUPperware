# TUPperware
A save editor for The Under Presents

## Downloading, Usage, and Modification
This section will tell you how to download, use, and modify the code of the program

### Download the program
If you just want to download and use the program, click on the green "Code" button in the top right, then "Download ZIP", then extract the ZIP archive.

If you want to download the program and intend to modify it, install Git on your machine and run the command ``` git clone https://github.com/SomeSpaceNerd/TUPperware.git ```.

### Usage
Step 1: Download and install Python 3.12 (or later) for your operating system from [Python's Website](https://www.python.org/downloads/).

Step 2:   
If you are on Windows, run the ``` TUPperware.bat ``` file to setup and run the program.

If you are on Linux or MacOS run the ``` TUPperware.sh ``` file to setup and run the program.

TODO: How to use the program

### Modification and Contributing
This program was made in QT Creator Community Edition 16.0.1 using Python 3.12 and PySide6.

I recommend using QT Creator to modify any part of the program, it can be downloaded from [QT's Website](https://www.qt.io/download-qt-installer-oss).
However, you can modify the mainwindow.py file in any normal IDE, but make sure you do not modify any UI files (like mainwindow.ui or ui_form.py) outside of QT Creator.

## Save File Notes
This section contains some notes about the save file's formatting and values.

### Cipher Key
The game encrypts a JSON file using a substitution cipher with the following key:   

| Ciphered Character  | Deciphered Character |
|---------------------|----------------------|
| Ì                   | a                    |
| ì                   | A                    |
| Ï                   | b                    |
| ï                   | B                    |
| Î                   | c                    |
| î                   | C                    |
| É                   | d                    |
| é                   | D                    |
| È                   | e                    |
| è                   | E                    |
| Ë                   | f                    |
| ë                   | F                    |
| Ê                   | g                    |
| ê                   | G                    |
| Å                   | h                    |
| å                   | H                    |
| Ä                   | i                    |
| ä                   | I                    |
| Ç                   | j                    |
| ç                   | J                    |
| Æ                   | k                    |
| æ                   | K                    |
| Á                   | l                    |
| á                   | L                    |
| À                   | m                    |
| à                   | M                    |
| Ã                   | n                    |
| ã                   | N                    |
| Â                   | o                    |
| â                   | O                    |
| Ý                   | p                    |
| ý                   | P                    |
| Ü                   | q                    |
| ü                   | Q                    |
| Ÿ                   | r                    |
| ÿ                   | R                    |
| ß                   | r                    |
| Þ                   | s                    |
| þ                   | S                    |
| Ù                   | t                    |
| ù                   | T                    |
| Ø                   | u                    |
| ø                   | U                    |
| Û                   | v                    |
| û                   | V                    |
| Ú                   | w                    |
| ú                   | W                    |
| Õ                   | x                    |
| õ                   | X                    |
| Ô                   | y                    |
| ô                   | Y                    |
| Z                   | Z                    |
| \u009D              | 0                    |
| \u009C              | 1                    |
| \u009F              | 2                    |
| \u009E              | 3                    |
| \u0099              | 4                    |
| \u0098              | 5                    |
| \u009B              | 6                    |
| \u009A              | 7                    |
| \u0095              | 8                    |
| \u0094              | 9                    |
| \u0083              | .                    |
| ò                   | _                    |
| Ö                   | {                    |
| Ð                   | }                    |
| ö                   | [                    |
| ð                   | ]                    |
| \u008F              | "                    |
| \u0097              | :                    |
| \u008D              | (space)              |
| \u0081              | ,                    |
| §                   | (newline)            |

### Mask Designs
The player's mask design is stored under cosmetics > maskDesign.  
The mask design is represented with numbers from 0-9:

| Number | Mask    |
|--------|---------|
| 0      | Chevron |
| 1      | Cyclops |
| 2      | Onion   |
| 3      | Druid   |
| 4      | Cheese  |
| 5      | VIP     |
| 6      | Crob    |
| 7      | Star    |
| 8      | Tempest |

**NOTICE: SETTING YOUR MASK DESIGN TO 1 OR 8 (CYCLOPS OR TEMPEST) COULD CAUSE YOU TO GET BANNED BECAUSE THEY ARE NORMALLY UNOBTAINABLE**

### Hats
The player's hat is stored under persistentHatDesign.   
The hat is represented with numbers from 0-33:   

| Number | Hat               |
|--------|-------------------|
| 0      | None              |
| 1      | Chef Hat          |
| 2      | Captain           |
| 3      | Flower Crown      |
| 4      | Ruffles           |
| 5      | Musketeer         |
| 6      | Antonio           |
| 7      | Pirate            |
| 8      | Goddess           |
| 9      | Hard Hat          |
| 10     | Sun Hat           |
| 11     | Feathers          |
| 12     | Flamingo Floaty   |
| 13     | Lemishine Hat     |
| 14     | Onion Hat         |
| 15     | Party Hat         |
| 16     | Coleman Hat       |
| 17     | Sun Hat Flowers   |
| 18     | Beanie            |
| 19     | Hamburger         |
| 20     | Cheese            |
| 21     | Halo              |
| 22     | Muskateer Low     |
| 23     | Party Hat Rainbow |
| 24     | Jester Hat        |
| 25     | Beret             |
| 26     | Hood              |
| 27     | Witch Hat         |
| 28     | Fried Egg Bonnet  |
| 29     | Cowboy Hat        |
| 30     | Tart Hat          |
| 31     | Flower Crown Low  |
| 32     | Bow Hat           |
| 33     | Boot Hat          |

## Known glitches and issues:
This section outlines the known issues that can occur from loading a modified save into the game.

1. Setting your mask design to 1 (Cyclops), or any number outside of the 0-9 range causes it to render without a front mesh (effectively being transparent from the front) and can cause other strange issues like players becoming invisible, or game crashes.
2. Setting your mask design to 5 (VIP) and going into the Timeboat photobooth without 100%ing Timeboat will result in you being stuck in the limbo/interlude room with the photobooth displaying the "1" texture on it's screen. In this glitched state, you are able to take your mask out of the tray and do magic.

## Disclaimer

TUPperware is an independent, open-source project released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). It is not affiliated with, endorsed by, or sponsored by Tender Claws or any of its partners. All trademarks, service marks, and copyrights related to *The Under Presents* are the property of their respective owners.

This software is provided solely for educational and research purposes. It is intended to help users better understand how *The Under Presents*' game save data works. The author does not condone or encourage using this tool to gain unauthorized access to paid content or to violate the terms of service of any game or platform.

By using this software, you agree that you do so at your own risk. The author is not responsible for any loss of save data, in-game progress, or consequences such as account suspension, banning, or any other penalties that may result from its use.

