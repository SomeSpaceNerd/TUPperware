# TUPperware
A graphical save editor for The Under Presents

## Downloading, Usage, and Modification
This section will tell you how to download, use, and modify the code of the program

### Downloading and Launching the Program
You can download the latest release executable file (TUPperware_Vx.y.z.exe) from the [releases page](https://github.com/SomeSpaceNerd/TUPperware/releases).   

#### Launching with verbose debugging
If there are unexpected errors or other issues occurring, you may want to enable verbose (debug) logging to have the program print more information about what it is doing.   
To do this, launch the executable with the ```-V``` or ```--verbose``` command line argument.

#### Antivirus False-Positive
This program may be classified as "Trojan:Win32/Wacatac.C!ml" upon download or launch, this is a false-positive.   
This program uses pyside6-deploy, a Nuitka based tool, to compile the python code and UI files into an executable.   
Nuitka is known to trigger antivirus false-positives due to its use of compressed data, and it's unfortunate prevalence in actual malware.   
If you are still concerned, you can look over all of the code in this repository and compile it into an executable yourself.   

Here are some links you may find useful:   
[Official acknowledgement of this issue](https://nuitka.net/user-documentation/common-issue-solutions.html#windows-virus-scanners)   
[Nuitka creator explaining why this occurs](https://github.com/Nuitka/Nuitka/issues/2685#issuecomment-1923357489)   
[VirusTotal scan of TUPperware V1.3.0 (I encourage you to actually look at what was flagged and by what engines to understand why flagging the program as malware is inaccurate)](https://www.virustotal.com/gui/file/d6f1fd34aea82be88124d5db4ec0d77373f8e0d7ac1540b055c6b9f46fe348d7/detection)

### Usage
#### Finding your save files
On Windows your save files are located in your user's appdata folder under ```LocalLow\Tender Claws\The Under Presents```   
You can open your AppData folder by pressing Win+R and running ```%USERPROFILE%\AppData```

On Quest your save files are located in ```sdcard/Android/Data/com.TenderClaws.TheUnderPresents.Quest/files```   
You can access that directory and download/upload your save files using [Sidequest](https://sidequestvr.com/download)

Download or copy/paste your save files into a folder like your documents folder so the program can access them.

**PLEASE MAKE UNMODIFIED BACKUPS OF YOUR SAVE FILES BEFORE MODIFYING THEM**

#### Importing a save file
Click on the top text box to open the file picker, select your save file, and click the "Load" button.

#### Modifying a save file
To modify any value in the save file, double click on it, enter in it's new value, and press enter.

#### Exporting a save file
Enable or disable ciphering the output with the checkbox at the bottom of the GUI.   
Ciphering the output is required if you want to load the modified save in-game.

Click on the bottom text box to open the file picker, select/create the file you want to output the modified save file to, and press the "Export" button.

If an there are issues with the values in your save file an error dialog will pop up during the export process, it is recommended to not skip past any errors, as it may cause in-game issues.   
Erroneous values that need to be changed will be highlighted in red in the tree widget, change them according to what the error message suggested.

### Building from Source and Modifying
This section only applies if you want to download the source code and make modifications, if you just want to run it look at the [Downloading and Launching section](#downloading-and-launching-the-program)

To download the program's source code, please install git and use the command ```git clone https://github.com/SomeSpaceNerd/TUPperware.git```

To build an executable file from the source code, install PySide6.8.3 using pip and then run the command ```pyside6-deploy -c pysidedeploy.spec``` inside the source directory   
Sometimes pyside6-deploy replaces relative paths (like main.py) with full paths (like /home/user/TUPperware/main.py), or adds to empty paths like the python directory in pysidedeploy.spec, please make sure you convert them back before committing to the repository.

This program was made in QT Creator Community Edition 16.0.2 using Python 3.12 and PySide6.8.3   
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
| \u0080              | -                    |
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

This key was found by reverse engineering my own save file, no decompilations or other unauthorized methods were used in the creation of this program and the cipher key it uses.

### Tutorial keys:
#### onboardingProgress
| Value | State                             |
|-------|-----------------------------------|
| 0     | None                              |
| 1     | UnderVisit_N1_fromHologram        |
| 2     | UnderVisit_N2_fromDemoShipTableau |
| 3     | UnderVisit_N3_fromRegularShip     |
| 4     | ElevatorPuzzleComplete            |

#### _desertTutorialCompleteExplicit
| Value | State                                      |
|-------|--------------------------------------------|
| True  | You have completed the desert tutorial     |
| False | You have not completed the desert tutorial |

#### mcShouldDoPostTableau
| Value | State                             |
|-------|-----------------------------------|
| True  | The MC should do post tableau     |
| False | The MC should not do post tableau |

#### mcShouldDoPhotoboothReminder
| Value | State                                        |
|-------|----------------------------------------------|
| True  | The MC should do the photobooth reminder     |
| False | The MC should not do the photobooth reminder |

#### restorationTutorialComplete
| Value | State                                           |
|-------|-------------------------------------------------|
| True  | You have completed the restoration tutorial     |
| False | You have not completed the restoration tutorial |

#### timeboatTutorialComplete
| Value | State                                        |
|-------|----------------------------------------------|
| True  | You have completed the Timeboat tutorial     |
| False | You have not completed the Timeboat tutorial |

### photobooth
#### termsAndConditionsScreenAccepted
| Value | State                                          |
|-------|------------------------------------------------|
| True  | You have accepted the terms and conditions     |
| False | You have not accepted the terms and conditions |

#### shouldDoTutorial
| Value | State                                            |
|-------|--------------------------------------------------|
| True  | You should do the tutorial on your next trip     |
| False | You should not do the tutorial on your next trip |

#### timesGoneToShip
| Value                 | State                                    |
|-----------------------|------------------------------------------|
| Positive whole number | How many times you have gone to Timeboat |

#### hasDoneInterludeTwo
| Value | State                           |
|-------|---------------------------------|
| True  | You have done interlude two     |
| False | You have not done interlude two |

#### hasDoneInterludeThree
| Value | State                             |
|-------|-----------------------------------|
| True  | You have done interlude three     |
| False | You have not done interlude three |

#### hasDoneInterludeFour
| Value | State                            |
|-------|----------------------------------|
| True  | You have done interlude four     |
| False | You have not done interlude four |

#### hasDoneInterludeFive
| Value | State                            |
|-------|----------------------------------|
| True  | You have done interlude five     |
| False | You have not done interlude five |

#### wentToInterludeLastTrip
| Value | State                                    |
|-------|------------------------------------------|
| True  | You went to an interlude last trip       |
| False | You did not go to an interlude last trip |

#### hasFinishedEpilogue
| Value | State                              |
|-------|------------------------------------|
| True  | You have finished the epilogue     |
| False | You have not finished the epilogue |

### giftshop
#### hasDoneFirstGiftshopEncounter
| Value | State                                          |
|-------|------------------------------------------------|
| True  | You have done the first giftshop encounter     |
| False | You have not done the first giftshop encounter |

#### hasDoneColemanGiftshopEncounter
| Value | State                                            |
|-------|--------------------------------------------------|
| True  | You have done the Coleman giftshop encounter     |
| False | You have not done the Coleman giftshop encounter |

#### hasDoneLabyrinthSuccessEncounter
| Value | State                                             |
|-------|---------------------------------------------------|
| True  | You have done the labyrinth success encounter     |
| False | You have not done the labyrinth success encounter |

### shipCharacterInfo
#### CookSaved
| Value | State                     |
|-------|---------------------------|
| True  | You saved the cook        |
| False | You did not save the cook |

#### SaraSaved
| Value | State                 |
|-------|-----------------------|
| True  | You saved Sara        |
| False | You did not save Sara |

#### ColemanSaved
| Value | State                    |
|-------|--------------------------|
| True  | You saved Coleman        |
| False | You did not save Coleman |

#### CaptainSaved
| Value | State                        |
|-------|------------------------------|
| True  | You saved the Captain        |
| False | You did not save the Captain |

#### AdelaSaved
| Value | State                  |
|-------|------------------------|
| True  | You saved Adela        |
| False | You did not save Adela |

#### ThewSaved
| Value | State                 |
|-------|-----------------------|
| True  | You saved Thew        |
| False | You did not save Thew |

#### RumphSaved
| Value | State                  |
|-------|------------------------|
| True  | You saved Rumph        |
| False | You did not save Rumph |

#### BillySaved
| Value | State                  |
|-------|------------------------|
| True  | You saved Billy        |
| False | You did not save Billy |

#### SandySaved
| Value | State                  |
|-------|------------------------|
| True  | You saved Sandy        |
| False | You did not save Sandy |

#### GeraldSaved
| Value | State                   |
|-------|-------------------------|
| True  | You saved Gerald        |
| False | You did not save Gerald |

### chapterUnlockInfo
#### firstChapterUnlocked
| Value | State                                   |
|-------|-----------------------------------------|
| True  | You have unlocked the first chapter     |
| False | You have not unlocked the first chapter |

#### secondChapterUnlocked
| Value | State                                    |
|-------|------------------------------------------|
| True  | You have unlocked the second chapter     |
| False | You have not unlocked the second chapter |

#### thirdChapterUnlocked
| Value | State                                   |
|-------|-----------------------------------------|
| True  | You have unlocked the third chapter     |
| False | You have not unlocked the third chapter |

#### fourthChapterUnlocked
| Value | State                                    |
|-------|------------------------------------------|
| True  | You have unlocked the fourth chapter     |
| False | You have not unlocked the fourth chapter |

### cosmetics
#### maskDesign
| Value  | Mask    |
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

**NOTICE: SETTING YOUR MASK DESIGN TO 1 OR 8 (CYCLOPS OR TEMPEST) COULD CAUSE YOU TO GET BANNED BECAUSE THEY ARE NORMALLY UNOBTAINABLE AS OF THE MOST RECENT VERSION**

### savedObjectives
#### hasUsedGiftshopExit
| Value | State                               |
|-------|-------------------------------------|
| True  | You have used the giftshop exit     |
| False | You have not used the giftshop exit |

#### numberOfAct1ScenesUnlocked
| Value                             | State                                                                  |
|-----------------------------------|------------------------------------------------------------------------|
| Positive or negative whole number | How many Act 1 scenes you have unlocked (-1 is none/tutorial/free demo)|

#### numberOfAct2ScenesUnlocked
| Value                             | State                                                                  |
|-----------------------------------|------------------------------------------------------------------------|
| Positive or negative whole number | How many Act 2 scenes you have unlocked (-1 is none/tutorial/free demo)|

#### numberOfAct3ScenesUnlocked
| Value                             | State                                                                  |
|-----------------------------------|------------------------------------------------------------------------|
| Positive or negative whole number | How many Act 3 scenes you have unlocked (-1 is none/tutorial/free demo)|

### multiplayerToggleInfo
#### timeOfLastToggle
| Value                          | State                                                                   |
|--------------------------------|-------------------------------------------------------------------------|
| Positive floating point number | The time when you last toggled multiplayer (Unity / C# datetime format) |

### tempestUserFlowData
#### HasVisitedTempestMarquee
| Value | State                                    |
|-------|------------------------------------------|
| True  | You have visited the Tempest Marquee     |
| False | You have not visited the Tempest Marquee |

#### HasVisitedTicketPurchaseUI
| Value | State                                               |
|-------|-----------------------------------------------------|
| True  | You have visited the Tempest Ticket Purchase UI     |
| False | You have not visited the Tempest Ticket Purchase UI |

#### HasSelectedMovementStyle
| Value | State                                             |
|-------|---------------------------------------------------|
| True  | You have selected your Tempest movement style     |
| False | You have not selected your Tempest movement style |

#### HasAcknowledgedFlashingLightsWarning
| Value | State                                                         |
|-------|---------------------------------------------------------------|
| True  | You have acknowledged the Tempest flashing lights warning     |
| False | You have not acknowledged the Tempest flashing lights warning |

#### UserMaskBeforeSwap
| Value                 | State                                         |
|-----------------------|-----------------------------------------------|
| Positive whole number | Your mask before swapping to the Tempest mask |

### persistentHatDesign
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

**NOTICE: SETTING YOUR HAT TO 3 OR 4 (FLOWER CROWN OR RUFFLES) COULD CAUSE YOU TO GET BANNED BECAUSE THEY ARE NORMALLY UNOBTAINABLE AS OF THE MOST RECENT VERSION**

### TLGameSettings
#### singlePlayerOfflineMode
| Value | State                                    |
|-------|------------------------------------------|
| True  | Single player / offline mode is enabled  |
| False | Single player / offline mode is disabled |

#### swapGrabAndSnapButtons
| Value | State                                 |
|-------|---------------------------------------|
| True  | Grab and snap buttons are swapped     |
| False | Grab ans snap buttons are not swapped |

#### use24HourTime
| Value | State                |
|-------|----------------------|
| True  | 24-Hour time is used |
| False | 12-Hour time is used |

#### scrunchStyle
| Value                 | State              |
|-----------------------|--------------------|
| Positive whole number | Your scrunch style |

#### strafeEnabled
| Value | State                |
|-------|----------------------|
| True  | Strafing is enabled  |
| False | Strafing is disabled |

## Known glitches and issues:
This section outlines the known issues that can occur from loading a modified save into the game.

1. Setting your mask design to 1 (Cyclops), or any number outside of the 0-9 range causes it to render without a front mesh (effectively being transparent from the front) and can cause other strange issues like players becoming invisible, or game crashes.
2. Setting your mask design to 5 (VIP) and going into the Timeboat photobooth without 100%ing Timeboat will result in you being stuck in the limbo/interlude room with the photobooth displaying the "1" texture on it's screen. In this glitched state, you are able to take your mask out of the tray and do magic.
3. Changing your mask before completing the tutorial will cause your mask to not update in-game.

All of these issues will be caught by the program before exporting your save file.

## Special thanks
Thank you to reddit user u/Elegant_League_7367 for proposing the idea of a save editor and for help testing it.   

## Disclaimer

TUPperware is an independent, open-source project released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). It is not affiliated with, endorsed by, or sponsored by Tender Claws or any of its partners. All trademarks, service marks, and copyrights related to *The Under Presents* are the property of their respective owners.

This software is provided solely for educational and research purposes. It is intended to help users better understand how *The Under Presents*' game save data works. The author does not condone or encourage using this tool to gain unauthorized access to paid content or to violate the terms of service of any game or platform.

By using this software, you agree that you do so at your own risk. The author is not responsible for any loss of save data, in-game progress, or consequences such as account suspension, banning, or any other penalties that may result from its use.


While this tool has not caused any account to be banned from online features in it's testing, the possibility of that occurring CANNOT be ruled out.

---
IRONS: 454-6000100
