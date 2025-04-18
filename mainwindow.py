# This Python file uses the following encoding: utf-8

version = "V0.1.0-alpha.2"
verbose_logging = True # If set to true, the program will log more information that may be useful for debugging

# Cipher table is complete but may not be accurate
# Syntax appears to be JSON
cipher_table = { # Cipher key, thanks to https://www.reddit.com/user/Elegant_League_7367/
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
    "UNKNOWN-Z": "Z",
    u"\u009F": "2",
    u"\u0099": "4",
    u"\u0094": "9", # Possibly a number, best guess
    u"\u0095": "8", # Possibly a number, best guess
    u"\u0098": "5", # Possibly a number, best guess
    u"\u009A": "7", # Possibly a number, best guess
    u"\u009B": "6", # Possibly a number, best guess
    u"\u009C": "1", # Possibly a number, best guess
    u"\u009D": "0", # Possibly a number, best guess
    u"\u009E": "3", # Possibly a number, best guess
    #u"\u0096": "10", # Possibly a number, was in my save file before but now isnt (?), placeholder
    u"\u0083": "_", # Possibly a syntax character, number, or just character (used in numbers, like Act1_XXXX) (This SHOULD be a number, there is a syntax error if it is not)
    "ò": "-", # Not a syntax character, used as a separator in strings
    "Ö": "{", # Syntax character, may be inaccurate
    "Ð": "}", # Syntax character, may be inaccurate
    "ö": "[", # Syntax character, may be inaccurate
    "ð": "]", # Syntax character, may be inaccurate
    u"\u008F": '"', # Syntax character, may be inaccurate (Note this is a double quote)
    u"\u0097": ":", # Syntax Character, may be inaccurate
    u"\u008D": " ", # Syntax Character, may be inaccurate
    u"\u0081": ",", # Syntax Character, may be inaccurate
    "§": " "  # Line separator/space character
}
inv_cipher_table = {v: k for k, v in cipher_table.items()} # Create an inverted cipher table for ciphering the output save file (THIS WILL NOT WORK RIGHT NOW)

# Imports
import sys
import logging
import json
from PySide6.QtWidgets import QApplication, QMainWindow
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

    def load_save(self):
        try:
            with open(self.ui.input_path_line_edit.text(), "r", encoding = "utf_8") as tl_game_save: # Open the save file
                # Check if the save is empty
                if not tl_game_save.read(1):
                    raise Exception("Invalid (empty or unreadable) input file")
                else:
                    self.log_message("Successfully loaded input file", "INFO")

                ciphered_save = tl_game_save.read()
                self.deciphered_save = "{" # THIS SHOULD BE "" BUT PYTHON DOES NOT READ FIRST Ö/{ CHARACTER
                # Decipher the save file
                for char in ciphered_save:
                    if char in cipher_table:
                        self.deciphered_save = self.deciphered_save + cipher_table.get(char)
                    else:
                        self.deciphered_save = self.deciphered_save + char
                        self.log_message("Found invalid character in save file", "WARNING")


                self.log_message("Finished deciphering save file", "INFO")
                self.log_message(f"Deciphered save data is {self.deciphered_save}", "DEBUG")
                self.parse_save()

        # Catch any errors that may occur while loading the save file
        except Exception as e:
            self.log_message(f"An error occured while loading the save file: {e}", "ERROR")

    def parse_save(self):
        try:
            self.log_message("Parsing save file...", "INFO")
            self.json_game_save = json.loads(self.deciphered_save) # Load the save as JSON
            for key in self.json_game_save:
                value_type = type(self.json_game_save[key])
                self.log_message(f"Type of value is {value_type}", "DEBUG")

        except Exception as e:
            self.log_message(f"An error occured while parsing the save file: {e}", "ERROR")


    def export_save(self):
        try:
            if self.cipher_output == True:
                output_save = ""
                for char in self.deciphered_save:
                    if char in inv_cipher_table:
                        output_save = output_save + inv_cipher_table.get(char)
                    else:
                        output_save = output_save + char
                        self.log_message(f"Found invalid character in save file: {char}", "WARNING")

            elif self.cipher_output == False:
                output_save = self.deciphered_save

            with open(self.ui.output_path_line_edit.text(), "w", encoding = "utf_8") as output_file:
                self.log_message("Exporting save file...", "INFO")
                output_file.write(output_save)
                self.log_message("Save file exported successfully", "INFO")

        # Catch any errors that may occur while exporting the save file
        except Exception as e:
            self.log_message(f"An error occured while exporting the save file: {e}", "ERROR")



        except Exception as e:
            self.log_message(f"An error occured while exporting the save file: {e}", "ERROR")

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
