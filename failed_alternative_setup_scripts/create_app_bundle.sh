#!/bin/bash

# Define the app bundle path
APP_DIR="/Users/bear/Desktop/KeystrokeCounterApp.app"

# Define the path to your Python script
PYTHON_SCRIPT_PATH="./keystroke_counter.py"

# 1. Create the App Bundle Directory Structure
mkdir -p "$APP_DIR/Contents/MacOS"

# 2. Create the Executable Script
echo "#!/bin/bash
/Users/bear/opt/anaconda3/envs/vsdefault/bin/python3.11 $PYTHON_SCRIPT_PATH" > "$APP_DIR/Contents/MacOS/KeystrokeCounter"

# Make it executable
chmod +x "$APP_DIR/Contents/MacOS/KeystrokeCounter"

# 3. Create an Info.plist File
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
<dict>
    <key>CFBundleExecutable</key>
    <string>KeystrokeCounter</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>" > "$APP_DIR/Contents/Info.plist"

echo "App bundle created at $APP_DIR"
