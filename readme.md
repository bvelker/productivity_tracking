Keystroke Counter
Track daily keystrokes for productivity insights.

Setup
Prerequisites
Ensure you have the following installed:

Python 3.x
Pip for Python 3 (usually comes with Python 3.x installations)
Dependencies
Before running the script, you need to install the required Python packages:

bash
Copy code
pip install pynput pyyaml matplotlib
Usage
Navigate to the Script Directory

If your script is in a directory named productivity_tracking, navigate to that directory:

bash
Copy code
cd /path/to/directory/productivity_tracking
Replace /path/to/directory/ with your specific path.

Run the Script

Execute the script using:

python3 keystroke_counter.py
The script will start recording keystrokes. To terminate the keystroke listening, press the esc key followed by del. On termination, the script will update the keystroke count for the day in a keystrokes.yaml file and display a graph of the recorded data.

Permissions Management
To monitor global keystrokes on macOS, the script requires additional accessibility permissions. Here's how to grant these permissions:

Open System Preferences

Click on the Apple icon in the top left corner of your screen and select System Preferences.

Go to Security & Privacy

Click on Security & Privacy and navigate to the Privacy tab.

Allow Accessibility Access

In the left sidebar, select Accessibility. Click the lock icon at the bottom to make changes (you might need to enter your system password). Once unlocked, click the + button, navigate to your Python executable (it could be /usr/local/bin/python3 or the path to your Python in a virtual environment), and add it. If you're using a specific virtual environment, be sure to select the Python executable within that environment.

Remember: After you've granted permissions, you may need to restart the script for the changes to take effect.

Additional Information
The script saves daily keystrokes in a keystrokes.yaml file.
When closed, it will also display a graphical representation of the recorded keystrokes over multiple days using matplotlib.
