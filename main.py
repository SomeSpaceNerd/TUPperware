# This Python file uses the following encoding: utf-8

version = "V1.3.0"
verbose_logging = False # If set to true, the program will log more information that may be useful for debugging

cipher_table = { # Cipher key, based on https://www.reddit.com/user/Elegant_League_7367/
    "Ì": "a",
    "ì": "A",
    "Ï": "b",
    "ï": "B",
    "Î": "c",
    "î": "C",
    "É": "d",
    "é": "D",
    "È": "e",
    "è": "E",
    "Ë": "f",
    "ë": "F",
    "Ê": "g",
    "ê": "G",
    "Å": "h",
    "å": "H",
    "Ä": "i",
    "ä": "I",
    "Ç": "j",
    "ç": "J",
    "Æ": "k",
    "æ": "K",
    "Á": "l",
    "á": "L",
    "À": "m",
    "à": "M",
    "Ã": "n",
    "ã": "N",
    "Â": "o",
    "â": "O",
    "Ý": "p",
    "ý": "P",
    "Ü": "q",
    "ü": "Q",
    "Ÿ": "r",
    "ÿ": "R",
    "ß": "r",
    "Þ": "s",
    "þ": "S",
    "Ù": "t",
    "ù": "T",
    "Ø": "u",
    "ø": "U",
    "Û": "v",
    "û": "V",
    "Ú": "w",
    "ú": "W",
    "Õ": "x",
    "õ": "X",
    "Ô": "y",
    "ô": "Y",
    "Z": "Z", # Never used in the game's save system (to the best of my knowledge) # Placeholder for PC save files
    u"\u009D": "0", # Correct (I think)
    u"\u009C": "1", # Correct
    u"\u009F": "2", # Correct
    u"\u009E": "3", # Correct
    u"\u0099": "4", # Correct
    u"\u0098": "5", # Correct
    u"\u009B": "6", # Correct
    u"\u009A": "7", # Correct
    u"\u0095": "8", # Correct
    u"\u0094": "9", # Possibly a number, best guess
    #u"\u0096": "10", # Possibly a number, was in my save file before but now isnt (?), placeholder
    u"\u0080": "-", # Used in numbers
    u"\u0083": ".", # Used in numbers
    "ò": "_", # Used as a prefix or seperator in strings ("_desertTutorialCompleteExplicit", "TUTORIAL_RewindOrFastforward"), likely an artifact from Newtonsoft JSON
    "Ö": "{",
    "Ð": "}",
    "ö": "[",
    "ð": "]",
    u"\u008F": '"', # Double quote
    u"\u0097": ":",
    u"\u008D": " ", # Space
    u"\u0081": ",",
    "§": "\n" # Newline
}
inv_cipher_table = {v: k for k, v in cipher_table.items()} # Creates an inverted cipher table for re-ciphering the output save file

# Imports
import sys
import os
import platform
import importlib
import logging
import json
from dictdiffer import diff
from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QMessageBox, QFileDialog, QAbstractItemView
from PySide6.QtCore import Qt, QTime, QFile, QIODevice, QTextStream, QStringConverter, QSaveFile, QOperatingSystemVersion, QCommandLineParser, QCommandLineOption, QObject, QEvent, QTimer, QDir, QItemSelectionModel
from PySide6.QtGui import QBrush, QColor

# Important:
# You need to run the following commands to generate the ui_form.py files
#     pyside6-uic form.ui -o ui_form.py
#     pyside6-uic form_android.ui -o ui_form_android.py

from ui_form       import Ui_MainWindow as Ui_Desktop_MainWindow
from ui_form_android import Ui_MainWindow as Ui_Android_MainWindow
from tooltips import tooltips_dict

# Platform detection
IS_NUITKA = "__compiled__" in globals()
IS_ANDROID = (QOperatingSystemVersion.currentType() == QOperatingSystemVersion.Android)

Ui_MainWindow = Ui_Android_MainWindow if IS_ANDROID else Ui_Desktop_MainWindow # Set the mainwindow depending on the platform

# Setup the logger
handler = logging.FileHandler("TUPperware.log", encoding = "utf-8", mode = "w+")
handler.setFormatter(logging.Formatter(fmt = "%(asctime)s:%(funcName)s:%(levelname)s: %(message)s", datefmt="%H:%M:%S"))
logger = logging.getLogger("TUPperware")
logger.addHandler(handler)

if verbose_logging == True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

_HIGHLIGHT_USER_ROLE = Qt.UserRole + 100  # custom role to mark highlighted items

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.log_message("Verbose/Debug logging is enabled", "DEBUG")
        if IS_ANDROID == False: print("       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@                        @@@@@@\n    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@                      @@@@@@\n  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    @@@@@@\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  @@@@@@\n@@@@@@@                                                      @@@@@@@@@@@@@@@@@                @@@@@@\n@@@@@@@                                                      @@@@@@@@@@@@@@@@@@               @@@@@@\n@@@@@@@                                                      @@@@@@@@@@ @@@@@@@@@             @@@@@@\n@@@@@@@@                                                    @@@@@@@@@@@   @@@@@@@@@           @@@@@@\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@         @@@@@@\n   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@       @@@@@@\n     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@         @@@@@@@@@     @@@@@@\n                           @@@@@@@@@@@@@                         @@@@@@           @@@@@@@@@   @@@@@@\n                             @@@@@@@@@@                          @@@@@@             @@@@@@@@  @@@@@@\n                             @@@@@@@@@@                          @@@@@@              @@@@@@@@@@@@@@@\n                             @@@@@@@@@@                          @@@@@@                @@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  @@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    @@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      @@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        @@@@ ")
        logger.log(logging.INFO, "\n       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@                        @@@@@@\n    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@                      @@@@@@\n  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    @@@@@@\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  @@@@@@\n@@@@@@@                                                      @@@@@@@@@@@@@@@@@                @@@@@@\n@@@@@@@                                                      @@@@@@@@@@@@@@@@@@               @@@@@@\n@@@@@@@                                                      @@@@@@@@@@ @@@@@@@@@             @@@@@@\n@@@@@@@@                                                    @@@@@@@@@@@   @@@@@@@@@           @@@@@@\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@         @@@@@@\n   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@       @@@@@@\n     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@@         @@@@@@@@@     @@@@@@\n                           @@@@@@@@@@@@@                         @@@@@@           @@@@@@@@@   @@@@@@\n                             @@@@@@@@@@                          @@@@@@             @@@@@@@@  @@@@@@\n                             @@@@@@@@@@                          @@@@@@              @@@@@@@@@@@@@@@\n                             @@@@@@@@@@                          @@@@@@                @@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  @@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    @@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      @@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        @@@@ ", stacklevel=1)
        self.log_message(f"TUPperware Save Editor {version} By SomeSpaceNerd", "INFO")
        self.log_message(f"Python version: {platform.python_version()}, IS_NUITKA: {IS_NUITKA}, IS_ANDROID: {IS_ANDROID}", "DEBUG")

        # Load tooltips
        try:
            self.tooltips = tooltips_dict
        except Exception as e:
            self.log_message(f"Error while loading tooltips: {e}", "WARNING")
            self.tooltips = {} # Assign the tooltips dictionary to an empty one to avoid causing more errors later on

        if IS_ANDROID == False: # PC
            self.ui.cipher_output_check_box.checkStateChanged.connect(self.update_cipher_output_option) # Connect update ciphered output function to the checkbox
            self._input_browse_filter = self.ClickToBrowseFilter(self.ui.input_path_line_edit, select_dir=False)
            self.ui.input_path_line_edit.installEventFilter(self._input_browse_filter)
            self.ui.input_path_line_edit.returnPressed.connect(self.load_save) # Connect pressing enter in the input path line edit to the load save function
            self._output_browse_filter = self.ClickToBrowseFilter(self.ui.output_path_line_edit, select_dir=False)
            self.ui.output_path_line_edit.installEventFilter(self._output_browse_filter)
            self.ui.output_path_line_edit.returnPressed.connect(self.export_save) # Connect pressing enter in the export path line edit to the export save function

        self.ui.load_file_push_button.clicked.connect(self.load_save) # Connect pressing the load file button to the load save function
        self.ui.export_push_button.clicked.connect(self.export_save) # Connect pressing the export file button to the export save function
        self.deciphered_save = "" # Define an empty deciphered save varible for other functions
        self.cipher_output = True # Define the default cipher output becuase the checkbox functions only update when it's clicked

    def load_save(self):
        try:
            if IS_ANDROID == False: self.input_file_path = self.ui.input_path_line_edit.text() # Get the input path from the GUI line edit (only on PC)

            if not self.input_file_path:
                raise Exception("You have not entered a path")

            tl_game_save = QFile(self.input_file_path) # Load the input file with QFile
            if not tl_game_save.open(QIODevice.ReadOnly | QIODevice.Text): # Check if the input file exists
                raise IOError(f"Cannot open input file: {tl_game_save.errorString()}")

            # Wrap in QTextStream so it can be read with UTF-8
            stream = QTextStream(tl_game_save)
            stream.setEncoding(QStringConverter.Encoding.Utf8)

            ciphered_save = stream.readAll() # Read the file
            stream.flush() # Flush the QTextStream
            tl_game_save.close() # Close the file

            # Check if the save file is valid
            if not ciphered_save:
                raise Exception("Empty or invalid save file")
            else:
                self.log_message("Successfully loaded save file", "INFO")
                self.log_message("Deciphering save file...", "INFO")

            # Decipher the save file
            self.deciphered_save = "" # Ensure the deciphered save variable is empty
            for char in ciphered_save: # Loop through the characters in the save file
                QApplication.processEvents() # Stop the GUI from hanging and appearing crashed while loading

                if char in cipher_table: # Check if the character is in the cipher table
                    self.deciphered_save = self.deciphered_save + cipher_table.get(char) # Decipher it if it is
                else:
                    self.deciphered_save = self.deciphered_save + char
                    if char in inv_cipher_table: # Check if the character is already deciphered
                        self.log_message("Found already deciphered character, ignoring", "INFO") # Ignore it
                    else: # Check if the file is invalid/unknown
                        self.log_message("Found invalid character in save file", "WARNING") # Ignore it and log a warning


            self.log_message("Finished deciphering save file", "INFO")
            self.log_message(f"Deciphered save data is {self.deciphered_save}", "DEBUG")
            self.parse_save() # Call the save parser after deciphering it

        except Exception as e: # Catch any errors that may occur while loading the save file
            if "unterminated string literal" in str(e): # This could cause undefined or incorrect behavior, but it fixes the windows path error for now. "Too bad!" - Valve Devs
                self.log_message("You have either attempted to load a nonexistant file or a file on a Windows filesystem, the program will continue regardless", "WARNING")
                self.parse_save()
            else:
                self.log_message(f"An error occured while loading the save file: {e}", "ERROR")

    def parse_save(self): # Save parsing and loading into GUI function
        try:
            self.log_message("Parsing save file...", "INFO")
            self.game_save = json.loads(self.deciphered_save) # Load the save as JSON
            self.ui.save_tree_widget.clear() # Clear the tree widget
            items = []

            # Detect which kind of save file was loaded using the first key
            first_key = list(self.game_save.keys())[0]
            self.log_message(f"First key: {first_key}", "DEBUG")
            if first_key == "onboardingProgress":
                self.file_type = "TLGameSave"
            elif first_key == "singlePlayerOfflineMode":
                self.file_type = "TLGameSettings"
            else:
                self.file_type = "unknown"
            self.log_message(f"Detected file type: {self.file_type}", "DEBUG")

            for key in self.game_save: # Loop through every key in the save file
                self.log_message(f"Parsing key {key}", "DEBUG")
                value = self.game_save[key]

                if isinstance(value, (str, int, float, bool)): # Check if that key's value is a string, integer, floating point number, or boolean
                    self.log_message("Key is str/int/float/bool", "DEBUG")
                    items.append(self.parse_str_int_float_bool(self.game_save, key)) # Call the str/int/float/bool handler and append it's output to the item list

                if isinstance(value, list): # Check if the key's value is a list
                    self.log_message("Key is list", "DEBUG")
                    items.append(self.parse_list(self.game_save, key)) # Call the list handler and append it's output to the item list

                if isinstance(value, dict): # Check if the key's value is a dictionary
                    self.log_message("Key is dict", "DEBUG")
                    items.append(self.parse_dict(self.game_save, key)) # Call the dictionary handler and append it's output to the item list

            self.ui.save_tree_widget.insertTopLevelItems(0, items) # Update the GUI with the items

        except Exception as e: # Catch any errors that may occur while parsing the save file
            self.log_message(f"An error occured while parsing the save file: {e}", "ERROR")

    # These functions parse through a dictionary and key and return a QTreeListItem
    # String, Integer, Floating Point, or Boolean parser function
    def parse_str_int_float_bool(self, dict, key):
        self.log_message("Called string/integer/float/bool handler", "DEBUG")
        item = QTreeWidgetItem([key, str(dict[key])]) # Setup an item

        # Add the appropriate tool tip to the item
        if key in self.tooltips:
            item.setToolTip(0, self.tooltips[key][0])
            item.setToolTip(1, self.tooltips[key][1])

        # Set the item's flags
        item.setFlags(
        Qt.ItemIsSelectable
        |Qt.ItemIsEditable
        |Qt.ItemIsDragEnabled
        |Qt.ItemIsDropEnabled
        |Qt.ItemIsUserCheckable
        |Qt.ItemIsEnabled) # Make it editable

        return item # Return the item

    # List parser function
    def parse_list(self, input_dict, key):
            self.log_message("Called list handler", "DEBUG")
            item = QTreeWidgetItem([str(key), ""]) # Ensure both columns exist: key and placeholder for value
            # Make the node itself editable/draggable/checkable
            item.setFlags(
                Qt.ItemIsSelectable
                | Qt.ItemIsEditable
                | Qt.ItemIsDragEnabled
                | Qt.ItemIsDropEnabled
                | Qt.ItemIsUserCheckable
                | Qt.ItemIsEnabled
            )

            data_list = input_dict[key] # Get the input list

            if not data_list: # If it is empty, set it to a placeholder empty value
                item = QTreeWidgetItem([str(key), "[EMPTY LIST]"])
            else:
                for index, list_item in enumerate(data_list): # Loop through every item in the list
                    self.log_message(f"Index {index} is {list_item}", "DEBUG")
                    idx_str = str(index)

                    if isinstance(list_item, (str, int, float, bool)): # If the item is a string, integer, floating point number, or boolean, call the str/float/int/bool handler
                        # Add the result of the handler as a child item
                        child_item = QTreeWidgetItem([idx_str, str(list_item)])
                        if list_item in self.tooltips:
                            child_item.setToolTip(1, self.tooltips[str(list_item)])
                        # Add editable flag to the leaf
                        child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)
                        item.addChild(child_item)

                    elif isinstance(list_item, list): # If the item is a list, call the list handler
                        # Use the actual index as the key to avoid duplicates
                        temp_dict = {idx_str: list_item}
                        nested_item = self.parse_list(temp_dict, idx_str)
                        item.addChild(nested_item) # Add the result of the handler as a child item

                    elif isinstance(list_item, dict): # If the item is a dictionary, call the dictionary handler
                        temp_dict = {idx_str: list_item}
                        nested_item = self.parse_dict(temp_dict, idx_str)
                        item.addChild(nested_item) # Add the result of the handler as a child item

            return item # Return the item

    # Dictionary parsing function
    def parse_dict(self, base_dict, base_key):
        self.log_message("Called dict handler", "DEBUG")
        item = QTreeWidgetItem([str(base_key), ""]) # Ensure both columns exist
        # Set the item's flags
        item.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
            | Qt.ItemIsEnabled
        )

        dictionary = base_dict[base_key] # Get the input dictionary
        for key, value in dictionary.items(): # Loop through every key/value pair in the dictionary
            self.log_message(f"Parsing sub key {key}", "DEBUG")
            if isinstance(value, (str, int, float, bool)): # Check if the key's value is a string, integer, floating point number or boolean
                item.addChild(self.parse_str_int_float_bool(dictionary, key)) # Call the srt/int/float/bool handler and add it's result as a child item
            elif isinstance(value, list): # Check if the key's value is a list
                item.addChild(self.parse_list({key: value}, key)) # Call the list handler and add it's result as a child item
            elif isinstance(value, dict): # Check if the key's value is a dictionary
                item.addChild(self.parse_dict({key: value}, key)) # Call the dictionary handler and add it's result as a child item

        return item # Return the item

    # Helper functions for exporting the modified save file
    # Converts the QTreeWidget data to JSON
    def tree_to_dict(self, tree_item):
        child_count = tree_item.childCount()
        self.log_message(f"Called tree to dictionary with tree item: {tree_item}", "DEBUG")
        self.log_message(f"Item has {child_count} children", "DEBUG")

        if child_count == 0: # Check if the item is a leaf node (has no child items)
            key = tree_item.text(0)
            value = tree_item.text(1)
            value_lower = value.strip().lower()

            # Convert the srting value of the node into the correct data type
            if value_lower == "true":
                return key, True
            elif value_lower == "false":
                return key, False
            elif value_lower == "null":
                return key, None
            elif value == "[EMPTY LIST]":
                return key, []
            else:
                try:
                    return key, json.loads(value)
                except:
                    return key, value
        else:
            key = tree_item.text(0)

            # Check if the node is a list based on it's key values (if it's a list they are ordered numbers 1, 2, 3...)
            is_list = True
            for i in range(child_count):
                child_key = tree_item.child(i).text(0)
                if not child_key.isdigit():
                    is_list = False
                    break

            if is_list:
                # Build list based on sorted numeric keys
                result_list = [None] * child_count
                for i in range(child_count):
                    child = tree_item.child(i)
                    index = int(child.text(0))
                    _, value = self.tree_to_dict(child)
                    result_list[index] = value
                return key, result_list

            else: # The node is a dictionary
                d = {}
                for i in range(child_count):
                    k, v = self.tree_to_dict(tree_item.child(i))
                    d[k] = v
                return key, d

    # Updates the main JSON game save variable from the QTreeWidget
    def update_json_from_tree(self):
        self.log_message("Updating JSON save variable from tree", "DEBUG")
        new_data = {} # Setup an empty dictionary for the new data
        for i in range(self.ui.save_tree_widget.topLevelItemCount()): # Loop through every item in the QTreeWidget
            item = self.ui.save_tree_widget.topLevelItem(i) # Get the top level item
            k, v = self.tree_to_dict(item) # Parse the item and get it's key/value
            new_data[k] = v # Append the item's data to the new dictionary
        self.log_message(f"Updated JSON save data is {new_data}", "DEBUG")

        # Check if the new save data is different from the input save data
        changes = [op for op in diff(json.loads(self.deciphered_save), new_data, expand=True) if op[0] == "change"]

        if not changes:
            self.log_message("Input and output save data is identical", "INFO")
        else:
            for _, path, (old, new_value) in changes:
                path_str = "/".join(str(p) for p in path) if isinstance(path, (list, tuple)) else str(path)
                self.log_message(f"Value at {path_str} changed from {old!r} -> {new_value!r}", "INFO")

                if isinstance(path, (list, tuple)):
                    # prefer the last string key in the path; if none, fall back to last element
                    key_name = None
                    for p in reversed(path):
                        if isinstance(p, str):
                            key_name = p
                            break
                    if key_name is None:
                        key_name = str(path[-1])  # last element (index or other) as fallback
                else:
                    key_name = str(path)

                key_name_list = key_name.split(".")
                key_name = key_name_list[-1]

                self.log_message(f"Key Name: {key_name}", "DEBUG")

                # Detect if a value's type was changed (this is always invalid)
                if type(old) is not type(new_value):
                    self.log_message(f"Value type change detected at {path_str}!", "ERROR")
                    self.highlight_item_by_key(self.ui.save_tree_widget, key_name)
                    result = self.show_error_dialog("Value type changed", f"The value at {path_str} ({new_value!r}) is of type {type(new_value).__name__}, but it must be of type {type(old).__name__}.\nThe export process cannot continue.")
                    if result == False:
                        self.log_message("Aborted from value type change error dialog", "INFO")
                        raise Exception("Aborted due to value type change")


        self.game_save = new_data # Set the global save data variable to the new save data

    # Function to export the save file
    def export_save(self):
        try:
            # Check if a save file has been loaded
            if not self.deciphered_save:
                raise Exception("You have not loaded a save file yet")

            self.clear_all_highlights(self.ui.save_tree_widget)

            if IS_ANDROID == False:
                self.output_file_path = self.ui.output_path_line_edit.text() # Get the output file path from the GUI (only on PC)

            self.update_json_from_tree() # Update the save data JSON from the GUI

            # Conflict checking
            if self.file_type == "TLGameSave": # TLGameSave checks
                # Changing mask design before completing onboarding
                if (self.game_save["onboardingProgress"] != 4) and (self.game_save["cosmetics"]["maskDesign"] != 0): # self.deciphered_save["cosmetics"]["maskDesign"]:
                    self.log_message(f"Found conflict between onboardingProgress ({self.game_save["onboardingProgress"]}) and maskDesign ({self.game_save["cosmetics"]["maskDesign"]})", "WARNING")
                    self.highlight_item_by_key(self.ui.save_tree_widget, "onboardingProgress")
                    self.highlight_item_by_key(self.ui.save_tree_widget, "maskDesign")
                    result = self.show_warning_dialog("Value Conflict", "Normally it is impossible for your mask to be changed before completing the tutorial.\nPlease consider changing onboardingProgress to 4 or reverting back to the Chevron mask (maskDesign: 0).")
                    if result == True:
                        pass
                    if result == False:
                        raise Exception("Canceled from value conflict warning dialog box")

                # Changing to VIP mask without 100% completing TimeBoat
                if (self.game_save["cosmetics"]["maskDesign"] == 5) and (all(self.game_save["shipCharacterInfo"].values()) == False):
                    self.log_message(f"Found conflict between shipCharacterInfo ({self.game_save["shipCharacterInfo"].values()}) and maskDesign (5)", "WARNING")
                    self.highlight_item_by_key(self.ui.save_tree_widget, "maskDesign")
                    self.highlight_item_by_key(self.ui.save_tree_widget, "shipCharacterInfo")
                    result = self.show_warning_dialog("Value Conflict", "Changing your mask to VIP (maskDesign: 5) before 100% completing TimeBoat can cause numerous in-game issues, only fixed via a reinstall.\nPlease consider setting all of the values in shipCharacterInfo to True or changing to any other mask.")
                    if result == True:
                        pass
                    if result == False:
                        raise Exception("Canceled from value conflict warning dialog box")

                # Cyclops mask
                if self.game_save["cosmetics"]["maskDesign"] == 1:
                    self.log_message("Found value issue with maskDesign (1)", "WARNING")
                    self.highlight_item_by_key(self.ui.save_tree_widget, "maskDesign")
                    result = self.show_warning_dialog("Value Warning", "Changing your mask to Cyclops (maskDesign: 1) can cause odd unintended behavior in-game including your mask not rendering properly, other players not rendering correctly, or game crashes.\nConsider changing to any other mask.")
                    if result == True:
                        pass
                    if result == False:
                        raise Exception("Canceled from value warning dialog box")

            export_data = json.dumps(self.game_save, indent=4) # Format the output data correctly

            # Cipher the output if it is enabled
            if self.cipher_output == True:
                output_save = ""
                for char in export_data:
                    QApplication.processEvents() # Stop the GUI from hanging and appearing crashed while exporting

                    if char in inv_cipher_table: # Loop through the inverted cipher table
                        output_save = output_save + inv_cipher_table.get(char) # Append the ciphered character to the output save data
                    else: # If the character is invalid/already ciphered
                        output_save = output_save + char
                        if char in cipher_table:
                            self.log_message("Found already ciphered character, ignoring", "WARNING")
                        else:
                            self.log_message(f"Found invalid character in save file: {char}", "WARNING")

            # Dont cipher the output if it is not requested
            elif self.cipher_output == False:
                output_save = export_data

            # Pre-export checks
            if (self.input_file_path == self.output_file_path) and (IS_ANDROID == False): # Check if the user is exporting to the same file they imported from
                # Show a warning dialog box and see if the user wants to continue (only on PC)
                result = self.show_warning_dialog("Warning", "You are attempting to export the save data to the same file you imported it from. This is highly not reccomended unless you have a seperate backup of your input save.\nIgnoring this warning could cause irrecoverable issues in-game.")

                if result == True:
                    pass
                if result == False:
                    raise Exception("Canceled from same path warning dialog box")

            elif QFile.exists(self.output_file_path) and (IS_ANDROID == False): # Check if the user is exporting to a file that already exists
                # Show a warning dialog box and see if the user wants to continue (only on PC)
                result = self.show_warning_dialog("Warning", "You are attempting to export the save data to file that already exists, if you continue it will be overwritten.")

                if result == True:
                    pass
                if result == False:
                    raise Exception("Canceled from overwriting warning dialog box")

            # Export the output save file
            self.log_message("Opening output file...", "INFO")

            if not self.output_file_path:
                raise Exception("You have not entered a path")

            output_file = QSaveFile(self.output_file_path) # Load the output file with QFile
            if not output_file.open(QIODevice.WriteOnly | QIODevice.Text): # Check if the output file exists
                raise IOError(f"Cannot open output file: {output_file.errorString()}")

            # Wrap in QTextStream so it can be exported with UTF-8
            stream = QTextStream(output_file)
            stream.setEncoding(QStringConverter.Encoding.Utf8)

            self.log_message("Writing output data to file", "INFO")
            stream << output_save # Write the output data to the output file
            stream.flush() # Flush the QTextStream

            if not output_file.commit(): # Check if the save file was written successfully
                raise IOError(f"Failed to commit output save: {output_file.errorString()}")
            self.log_message("Save file exported successfully", "INFO")

        # Catch any errors that may occur while exporting the save file
        except Exception as e:
            self.log_message(f"An error occured while exporting the save file: {e}", "ERROR")

    def show_warning_dialog(self, title, text):
        # Create the message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning) # Set warning icon
        msg_box.setWindowTitle(title) # Set window title
        msg_box.setText(text) # Main text

        # Add custom buttons
        proceed_button = msg_box.addButton("Continue", QMessageBox.AcceptRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)

        msg_box.setDefaultButton(cancel_button) # Default focus on Cancel
        msg_box.setEscapeButton(cancel_button) # Hitting Esc triggers Cancel

        msg_box.exec()  # Open as a modal dialog so it cannot be closed

        # Determine which button was clicked
        if msg_box.clickedButton() == proceed_button:
            self.log_message("Proceeding past warning dialog", "DEBUG")
            return True
        else:
            self.log_message("Aborting operation", "DEBUG")
            return False

    def show_error_dialog(self, title, text):
        # Create the message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical) # Set error icon
        msg_box.setWindowTitle(title) # Set window title
        msg_box.setText(text) # Main text

        # Add custom buttons
        cancel_button = msg_box.addButton("Abort", QMessageBox.RejectRole)

        msg_box.setDefaultButton(cancel_button) # Default focus on Cancel
        msg_box.setEscapeButton(cancel_button) # Hitting Esc triggers Cancel

        msg_box.exec()  # Open as a modal dialog so it cannot be closed

        if msg_box.clickedButton() == cancel_button:
            self.log_message("Aborting Operation", "DEBUG")
            return False

    # Function to enable/disable ciphering the output depending on the GUI checkbox
    def update_cipher_output_option(self, state):
        if state == Qt.Checked:
            self.cipher_output = True
            self.log_message("Enabled cipher output", "INFO")
        else:
            self.cipher_output = False
            self.log_message("Disabled cipher output", "INFO")

    # Helper function to log messages to both the in-app console and log file
    def log_message(self, message, log_level):
        # Format message for the console
        console_message = f"""[{QTime.currentTime().toString("HH:mm:ss")}][{log_level}]: {message}"""
        # Display the message to the console
        if log_level != "DEBUG" or verbose_logging:
            self.ui.log_text_browser.append(console_message)
            scrollbar = self.ui.log_text_browser.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

            if IS_ANDROID == False: # Prevent double logging because logging and print both go to one log
                print(console_message)

        # Log the message to the log file
        exec(f"""logger.log(logging.{log_level}, "{message}", stacklevel=3)""")

    # Functions to highlight and select items in tree
    def _iter_descendants(self, root: QTreeWidgetItem):
        stack = [root]
        while stack:
            parent = stack.pop()
            for i in range(parent.childCount()):
                child = parent.child(i)
                yield child
                stack.append(child)

    def _clear_highlight(self, tree: QTreeWidget, item: QTreeWidgetItem, key_column: int) -> None:
        tree.blockSignals(True)
        try:
            # clear the item itself
            for c in range(max(1, tree.columnCount())):
                item.setBackground(c, QBrush())  # reset background
            item.setData(key_column, _HIGHLIGHT_USER_ROLE, None)
            idx = tree.indexFromItem(item, key_column)
            if idx.isValid() and tree.selectionModel() is not None:
                tree.selectionModel().select(idx, QItemSelectionModel.Deselect | QItemSelectionModel.Rows)
            if tree.currentItem() is item:
                tree.setCurrentItem(None)

            # also clear all descendants (children, grandchildren, ...)
            for child in self._iter_descendants(item):
                for c in range(max(1, tree.columnCount())):
                    child.setBackground(c, QBrush())
                child.setData(key_column, _HIGHLIGHT_USER_ROLE, None)
                cidx = tree.indexFromItem(child, key_column)
                if cidx.isValid() and tree.selectionModel() is not None:
                    tree.selectionModel().select(cidx, QItemSelectionModel.Deselect | QItemSelectionModel.Rows)
                if tree.currentItem() is child:
                    tree.setCurrentItem(None)
        finally:
            tree.blockSignals(False)


    def _ensure_highlight_handler(self, tree: QTreeWidget, key_column: int = 0) -> None:
        if getattr(tree, "_highlight_handler_installed", False):
            return

        def _on_item_changed(changed_item: QTreeWidgetItem) -> None:
            # 1) If the changed item itself is highlighted, remove its highlight.
            try:
                marked_self = bool(changed_item.data(key_column, _HIGHLIGHT_USER_ROLE))
            except Exception:
                marked_self = False
            if marked_self:
                self._clear_highlight(tree, changed_item, key_column)

            # 2) If any ancestor is highlighted, clear highlight on those ancestors
            #    (a change to a subkey should remove parent's highlight).
            p = changed_item.parent()
            while p is not None:
                try:
                    marked_parent = bool(p.data(key_column, _HIGHLIGHT_USER_ROLE))
                except Exception:
                    marked_parent = False
                if marked_parent:
                    self._clear_highlight(tree, p, key_column)
                p = p.parent()

            # 3) (Optional) logic to clear highlighted descendants if needed is left commented
            #    in case you want changes to a parent to remove descendant highlights.

        tree.itemChanged.connect(_on_item_changed)
        tree._highlight_handler_installed = True

    def highlight_item_by_key(
        self,
        tree: QTreeWidget,
        key: str,
        column: int = 0,
        select: bool = True,
        expand_parents: bool = True,
        scroll_to: bool = True
    ) -> bool:
        # ensure handler to remove highlight on change
        self._ensure_highlight_handler(tree, key_column=column)

        red_brush = QBrush(QColor("red"))

        # Walk the tree (DFS) to find the first matching item
        root = tree.invisibleRootItem()
        stack = [root]
        while stack:
            parent = stack.pop()
            for i in range(parent.childCount()):
                item = parent.child(i)
                if item.text(column) == key:
                    # expand parents so item is visible
                    if expand_parents:
                        p = item.parent()
                        while p is not None:
                            p.setExpanded(True)
                            p = p.parent()

                    # Set background and mark the item as highlighted.
                    # Block signals so our setBackground/setData doesn't trigger itemChanged handler.
                    tree.blockSignals(True)
                    try:
                        for c in range(max(1, tree.columnCount())):
                            item.setBackground(c, red_brush)
                            item.setData(column, _HIGHLIGHT_USER_ROLE, True)

                        for child in self._iter_descendants(item):
                                    for c in range(max(1, tree.columnCount())):
                                        child.setBackground(c, red_brush)
                                        child.setData(column, _HIGHLIGHT_USER_ROLE, True)

                    finally:
                        tree.blockSignals(False)

                    # Ensure selection mode allows multiple selections
                    if tree.selectionMode() == QAbstractItemView.SingleSelection:
                        tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

                    # add to selection without clearing existing selections
                    if select and tree.selectionModel() is not None:
                        idx = tree.indexFromItem(item, column)
                        if idx.isValid():
                            tree.selectionModel().select(idx, QItemSelectionModel.Select | QItemSelectionModel.Rows)
                            tree.setCurrentItem(item)

                        for child in self._iter_descendants(item):
                            cidx = tree.indexFromItem(child, column)
                            if cidx.isValid():
                                tree.selectionModel().select(cidx, QItemSelectionModel.Select | QItemSelectionModel.Rows)

                    if scroll_to:
                        tree.scrollToItem(item)

                    return True

                # push children to stack
                stack.append(item)

        return False

    def clear_all_highlights(self, tree: QTreeWidget, key_column: int = 0) -> None:
        tree.blockSignals(True)
        try:
            root = tree.invisibleRootItem()
            stack = [root]
            while stack:
                parent = stack.pop()
                for i in range(parent.childCount()):
                    item = parent.child(i)
                    # clear background
                    for c in range(max(1, tree.columnCount())):
                        item.setBackground(c, QBrush())
                    # clear highlight flag
                    item.setData(key_column, _HIGHLIGHT_USER_ROLE, None)
                    stack.append(item)
            # clear all selection
            if tree.selectionModel() is not None:
                tree.selectionModel().clearSelection()
            tree.setCurrentItem(None)
        finally:
            tree.blockSignals(False)

    # Class to allow for LineEdit single click/double click functions
    class ClickToBrowseFilter(QObject):
        def __init__(self, line_edit, select_dir=False):
            super().__init__(line_edit)
            self.line_edit = line_edit
            self.select_dir = select_dir
            self._double_clicked = False
            self._timer = QTimer(self)
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self._on_single_click_timeout)

        def eventFilter(self, obj, event):
            # Only handle events for the attached line edit
            if obj is not self.line_edit:
                return False

            # start a single-shot timer on press and cancel it on double-click
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self._double_clicked = False
                interval = QApplication.instance().doubleClickInterval()
                self._timer.start(interval)
                # return False so the line edit also receives the press (keeps focus/selection)
                return False

            if event.type() == QEvent.MouseButtonDblClick and event.button() == Qt.LeftButton:
                # stop the pending single-click action and let default double-click handling run
                self._timer.stop()
                self._double_clicked = True
                return False

            return False  # don't swallow other events

        def _on_single_click_timeout(self):
            # if a double-click happened, do nothing
            if self._double_clicked:
                return

            # open the appropriate dialog and set path if chosen
            start = self.line_edit.text() or QDir.homePath()
            if self.select_dir:
                path = QFileDialog.getExistingDirectory(self.line_edit, "Select folder", start)
                if path:
                    self.line_edit.setText(path)
            else:
                path, _ = QFileDialog.getOpenFileName(self.line_edit, "Select file", start)
                if path:
                    self.line_edit.setText(path)


if __name__ == "__main__": # If the program is being run as main
    app = QApplication(sys.argv) # Setup the QApplication

    # Command Line Arguments
    parser = QCommandLineParser()
    parser.setApplicationDescription("TUPperware Save Editor")
    app.setApplicationVersion(version)
    parser.addHelpOption()   # adds -h/--help
    parser.addVersionOption()

    verbose_option = QCommandLineOption(["verbose", "V"], "Enable verbose (debug) logging.")
    parser.addOption(verbose_option)

    parser.process(app)  # read argv from QApplication

    # set the global flag based on CLI option
    if parser.isSet(verbose_option):
        verbose_logging = True

    widget = MainWindow() # Setup the GUI
    widget.show() # Show the GUI
    sys.exit(app.exec()) # Execute all of the associated code and exit when closed
