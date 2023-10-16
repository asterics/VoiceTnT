# VoiceTnT

Voice Translate & Type (VoiceTnT) detects speech from the system's default microphone, 
translates it into another language or types the recognized text (using keyboard emulation).


The program functions are controlled via hotkeys (keyboard shortcuts):

* Hotkey-1: recognize a phrase in language 1
* Hotkey-2: recognize a phrase in language 2
* Hotkey-3: switch between translation mode and keyboard mode
* Esc: exit program

In translation mode, the recognized phrase is translated and spoken in the other language.
In keyboard mode, the recognized phrase is typed via keyboard emulation (so that the text is inserted into the application window or text field which currently has the focus).
The default mode is translation.


The hotkeys are stored in the textfile `hotkeys.txt`. New hotkeys can be recorded by using commandline argument ´-r´ (see below).
The default hotkeys are `Alt+1`,`Alt+2` and `Alt+3`.


## Installation and Prerequisites

* download .zip or clone the project repository
* open command prompt (shell window) in the project's subfolder
* install required packages in a Python3 environment: `pip install -r requirements.txt`
* run the script: `python VoiceTnT.py [-l1 <langID>] [-l2 <langID>] [-t] [-r]`


## Commandline arguments

The commandline arguments are optional:

* -l1: first language ID (default: de)
* -l2: second language ID (default: ro)
* -k: start in keyboard mode (default is translation mode)
* -r: record new hotkeys

Note: The `start.bat` script runs VoiceTnT with fixed arguments in a minimized window (only applicable under Windows).


