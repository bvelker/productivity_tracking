#!/bin/bash

# Path to the Python script
SCRIPT_PATH="/Users/bear/Desktop/productivity_tracking/keystroke_counter.py"

# AppleScript content to create the Automator app
APPLESCRIPT_CONTENT="
tell application \"Automator\"
	activate
	make new document at front
	delay 2
end tell
tell application \"System Events\"
	tell process \"Automator\"
		click menu item \"Run Shell Script\" of menu \"Actions\" of menu bar item \"Library\" of menu bar 1
		delay 1
		set value of text area 1 of scroll area 1 of group 1 of splitter group 1 of window 1 to \"/Users/bear/opt/anaconda3/envs/vsdefault/bin/python3.11 $SCRIPT_PATH\"
	end tell
end tell"

# Execute AppleScript
osascript -e "$APPLESCRIPT_CONTENT"

echo "Please save the Automator app manually as KeystrokeCounterApp.app on your Desktop or other preferred location."

