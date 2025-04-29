# This Python file uses the following encoding: utf-8

version = "V1.0.0-beta.2"
verbose_logging = True # If set to true, the program will log more information that may be useful for debugging

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
    "Z": "Z", # Never used in the game's save system (to the best of my knowledge)
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
    u"\u0083": ".", # Used in numbers
    "ò": "_", # Used as a prefix or seperator in strings ("_desertTutorialCompleteExplicit", "TUTORIAL_RewindOrFastforward"), likely an artifact from Newtonsoft JSON
    "Ö": "{",
    "Ð": "}",
    "ö": "[",
    "ð": "]",
    u"\u008F": '"', # Note that this is a double quote
    u"\u0097": ":",
    u"\u008D": " ", # Note that this is a space
    u"\u0081": ",",
    "§": "\n"
}
inv_cipher_table = {v: k for k, v in cipher_table.items()} # Creates an inverted cipher table for re-ciphering the output save file

# Imports
import sys
import logging
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QMessageBox
from PySide6.QtCore import Qt, QTime

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py

from ui_form import Ui_MainWindow

# Setup the logger
if verbose_logging == True:
    logging.basicConfig(filename= "TUPperware.log", filemode= "w", level= logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s", datefmt="%H:%M:%S")
else:
    logging.basicConfig(filename= "TUPperware.log", filemode= "w", level= logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.log_message(f"TUPperware Save Editor {version} By SomeSpaceNerd", "INFO")
        self.ui.cipher_output_check_box.checkStateChanged.connect(self.update_cipher_output_option) # Connect update ciphered output function to the checkbox
        # Connect the load save file button and pressing enter in the line edit to the load save function
        self.ui.load_file_push_button.clicked.connect(self.load_save)
        self.ui.input_path_line_edit.returnPressed.connect(self.load_save)
        # Connect the export save fule button and pressing enter in the line edit to the export save function
        self.ui.export_push_button.clicked.connect(self.export_save)
        self.ui.output_path_line_edit.returnPressed.connect(self.export_save)
        self.deciphered_save = "" # Define an empty deciphered save varible for other functions
        self.cipher_output = True # Define the default cipher output becuase the checkbox functions only update when its clicked

    def load_save(self):
        try:
            self.input_file_path = self.ui.input_path_line_edit.text()
            with open(self.input_file_path, "r", encoding = "utf_8") as tl_game_save: # Open the save file
                ciphered_save = tl_game_save.read()
                # Check if the save file is valid
                if not ciphered_save:
                    raise Exception("Empty or invalid save file")
                else:
                    self.log_message("Successfully loaded save file", "INFO")
                    self.log_message("Deciphering save file...", "INFO")

                # Decipher the save file
                self.deciphered_save = "" # Ensure the deciphered save variable is empty
                for char in ciphered_save:
                    # THIS SHOULD BE UNCOMMENTED BUT WINDOWS PATHS CAUSE AN ERROR HERE TOO
                    # QApplication.processEvents() # Stop the GUI from hanging and appearing crashed while loading

                    if char in cipher_table:
                        self.deciphered_save = self.deciphered_save + cipher_table.get(char)
                    else:
                        self.deciphered_save = self.deciphered_save + char
                        if char in inv_cipher_table:
                            self.log_message("Found already deciphered character, ignoring", "INFO")
                        else:
                            self.log_message("Found invalid character in save file", "WARNING")


                self.log_message("Finished deciphering save file", "INFO")
                self.log_message(f"Deciphered save data is {self.deciphered_save}", "DEBUG")
                self.parse_save()

        # Catch any errors that may occur while loading the save file
        except Exception as e:
            self.log_message(f"An error occured while loading the save file: {e}", "ERROR")
            self.parse_save() # TEMPORARY HACKY FIX BECAUSE WINDOWS PATHS ALWAYS CAUSES ERROR EVEN WHEN THE FILE IS LOADED CORRECTLY

    def parse_save(self):
        try:
            self.log_message("Parsing save file...", "INFO")
            self.json_game_save = json.loads(self.deciphered_save) # Load the save as JSON
            self.ui.save_tree_widget.clear() # Clear the tree widget
            items = []
            for key in self.json_game_save:
                self.log_message(f"Parsing key {key}", "DEBUG")
                value = self.json_game_save[key]

                if isinstance(value, (str, int, float, bool)):
                    self.log_message("Key is str/int/bool", "DEBUG")
                    items.append(self.parse_str_int_float_bool(self.json_game_save, key))

                if isinstance(value, list):
                    self.log_message("Key is list", "DEBUG")
                    items.append(self.parse_list(self.json_game_save, key))

                if isinstance(value, dict):
                    self.log_message("Key is dict", "DEBUG")
                    items.append(self.parse_dict(self.json_game_save, key))

            self.ui.save_tree_widget.insertTopLevelItems(0, items)

        except Exception as e:
            self.log_message(f"An error occured while parsing the save file: {e}", "ERROR")

    # These functions parse through a dictionary and key and return a QTreeListItem
    # String, Integer, Floating Point, or Boolean parser function
    def parse_str_int_float_bool(self, dict, key):
        self.log_message("Called string/integer/floating point/bool handler", "DEBUG") # Log a debug message
        item=QTreeWidgetItem([key, str(dict[key])]) # Setup an item
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled) # Make it editable
        return item # Return the item

    # List parser function
    def parse_list(self, input_dict, key):
            self.log_message("Called list handler", "DEBUG")
            # Ensure both columns exist: key and placeholder for value
            item = QTreeWidgetItem([str(key), ""])  # :contentReference[oaicite:0]{index=0}
            # Make the node itself editable/draggable/checkable
            item.setFlags(
                Qt.ItemIsSelectable
                | Qt.ItemIsEditable
                | Qt.ItemIsDragEnabled
                | Qt.ItemIsDropEnabled
                | Qt.ItemIsUserCheckable
                | Qt.ItemIsEnabled
            )

            data_list = input_dict[key]
            for index, list_item in enumerate(data_list):
                self.log_message(f"Index {index} is {list_item}", "DEBUG")
                idx_str = str(index)

                if isinstance(list_item, (str, int, float, bool)):
                    child_item = QTreeWidgetItem([idx_str, str(list_item)])
                    # Add editable flag to the leaf
                    child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)
                    item.addChild(child_item)

                elif isinstance(list_item, list):
                    # Use the actual index as the key to avoid duplicates
                    temp_dict = {idx_str: list_item}
                    nested_item = self.parse_list(temp_dict, idx_str)
                    item.addChild(nested_item)

                elif isinstance(list_item, dict):
                    temp_dict = {idx_str: list_item}
                    nested_item = self.parse_dict(temp_dict, idx_str)
                    item.addChild(nested_item)

            return item

    def parse_dict(self, base_dict, base_key):
        self.log_message("Called dict handler", "DEBUG")
        # Ensure both columns exist
        item = QTreeWidgetItem([str(base_key), ""])
        item.setFlags(
            Qt.ItemIsSelectable
            | Qt.ItemIsEditable
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsUserCheckable
            | Qt.ItemIsEnabled
        )

        dictionary = base_dict[base_key]
        for key, value in dictionary.items():
            self.log_message(f"Parsing sub key {key}", "DEBUG")
            if isinstance(value, (str, int, float, bool)):
                item.addChild(self.parse_str_int_float_bool(dictionary, key))
            elif isinstance(value, list):
                item.addChild(self.parse_list({key: value}, key))
            elif isinstance(value, dict):
                item.addChild(self.parse_dict({key: value}, key))

        return item

    # Helper functions for exporting the modified save file
    # Converts the QTreeWidget data to JSON
    def tree_to_dict(self, tree_item):
        child_count = tree_item.childCount()
        self.log_message(f"Called tree to dictionary with tree item: {tree_item}", "DEBUG")
        self.log_message(f"Item has {child_count} children", "DEBUG")

        if child_count == 0:
            # Leaf node
            key = tree_item.text(0)
            value = tree_item.text(1)
            value_lower = value.strip().lower()
            if value_lower == "true":
                return key, True
            elif value_lower == "false":
                return key, False
            elif value_lower == "null":
                return key, None
            else:
                try:
                    return key, json.loads(value)
                except:
                    return key, value
        else:
            key = tree_item.text(0)

            # Determine if it's a list: all children have numeric keys (like "0", "1", "2", ...)
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
            else:
                # Normal dictionary
                d = {}
                for i in range(child_count):
                    k, v = self.tree_to_dict(tree_item.child(i))
                    d[k] = v
                return key, d

    # Updates the main JSON game save variable from the QTreeWidget
    def update_json_from_tree(self):
        self.log_message("Updating JSON save variable from tree", "DEBUG")
        new_data = {}
        for i in range(self.ui.save_tree_widget.topLevelItemCount()):
            item = self.ui.save_tree_widget.topLevelItem(i)
            k, v = self.tree_to_dict(item)
            new_data[k] = v
        self.log_message(f"Updated JSON save data is {new_data}", "DEBUG")
        self.json_game_save = new_data

    def export_save(self):
        try:
            # Check if a save file has been loaded
            if not self.deciphered_save:
                raise Exception("You have not loaded a save file yet")

            self.output_file_path = self.ui.output_path_line_edit.text()
            if self.input_file_path == self.output_file_path: # Check if the user is exporting to the same file they imported from
                # Show a warning dialog box and see if the user wants to continue
                result = self.show_warning_dialog("Warning", "You are attempting to export the save data to the same file you imported it from. This is highly not reccomended unless you have a seperate backup of your input save.\nIgnoring this warning could cause irrecoverable issues in-game.")

                if result == True:
                    pass
                if result == False:
                    raise Exception("Canceled from warning dialog box")

            self.update_json_from_tree()
            export_data = json.dumps(self.json_game_save, indent=4)

            # Cipher the output if it is enables
            if self.cipher_output == True:
                output_save = ""
                for char in export_data:
                    # THIS SHOULD BE UNCOMMENTED BUT WINDOWS PATHS CAUSE AN ERROR HERE TOO
                    # QApplication.processEvents() # Stop the GUI from hanging and appearing crashed while exporting

                    if char in inv_cipher_table:
                        output_save = output_save + inv_cipher_table.get(char)
                    else:
                        output_save = output_save + char
                        if char in cipher_table:
                            self.log_message("Found already ciphered character, ignoring", "WARNING")
                        else:
                            self.log_message(f"Found invalid character in save file: {char}", "WARNING")

            # Dont cipher the output if it is not requested
            elif self.cipher_output == False:
                output_save = export_data

            # Export the output save file
            with open(self.ui.output_path_line_edit.text(), "w", encoding = "utf_8") as output_file:
                self.log_message("Exporting save file...", "INFO")
                output_file.write(output_save)
                self.log_message("Save file exported successfully", "INFO")

        # Catch any errors that may occur while exporting the save file
        except Exception as e:
            self.log_message(f"An error occured while exporting the save file: {e}", "ERROR")

    def show_warning_dialog(self, title, text):
        # Create the message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)          # Set warning icon
        msg_box.setWindowTitle(title)              # Window title
        msg_box.setText(text)  # Main text

        # Add custom buttons
        proceed_button = msg_box.addButton("Continue", QMessageBox.AcceptRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)

        msg_box.setDefaultButton(cancel_button)        # Default focus on Cancel
        msg_box.setEscapeButton(cancel_button)         # Hitting Esc triggers Cancel

        msg_box.exec()  # Open as a **modal** dialog

        # Determine which button was clicked
        if msg_box.clickedButton() == proceed_button:
            self.log_message("Proceeding past warning dialog", "DEBUG")
            return True
        else:
            self.log_message("Aborting operation", "DEBUG")
            return False

    # Function to enable/disable ciphering the output depending on the UI checkbox
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
        console_message = f"[{QTime.currentTime().toString("HH:mm:ss")}][{log_level}]: {message}"
        # Display the message to the console
        if log_level != "DEBUG" or verbose_logging:
            self.ui.log_text_browser.append(console_message)
            scrollbar = self.ui.log_text_browser.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            print(console_message)

        # Log the message to the log file
        lowercase_log_level = log_level.lower()
        exec(f"""logger.{lowercase_log_level}("{message}")""")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
