# TUPperware
A save editor for The Under Presents

## Downloading, Usage, and Modification
This section will tell you how to download, use, and modify the code of the program

### Download the program
If you just want to download and use the program, click on the green "Code" button in the top left, then "Download ZIP", then extract the ZIP archive   
If you want to download the program and intend to modify it, install Git on your machine and run the command ``` git clone https://github.com/SomeSpaceNerd/TUPperware.git ```

### Usage
Step 1: Download and install Python 3.12 (or later) for your operating system from [Python's Website](https://www.python.org/downloads/)

TODO

## Save File Notes
This section contains some notes about the save file's formatting and values

### Cipher Key
The game encrypts a JSON file using a substitution cipher with the following key   

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
The player's mask design is stored under cosmetics > maskDesign   
The mask design is represented with numbers from 0-9

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
The player's hat is stored under persistentHatDesign   
The hat is represented with numbers from 0-33   

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

