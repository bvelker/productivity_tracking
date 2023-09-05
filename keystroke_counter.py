import os
import yaml
from pynput.keyboard import Key, Listener
import datetime
import matplotlib.pyplot as plt
import logging

# Define the working directory and log file path
working_directory = os.path.join("/Users/bear/Desktop/productivity_tracking/", "working_directory")
log_file_path = os.path.join(working_directory, "log_file.log")

# Ensure working_directory exists
if not os.path.exists(working_directory):
    os.makedirs(working_directory)

logging.basicConfig(filename=log_file_path, level=logging.INFO)
logging.info('Script started.')

# Update the path for KEYSTROKES_FILE
KEYSTROKES_FILE = os.path.join(working_directory, 'keystrokes.yaml')

keystrokes = 0
current_date = datetime.date.today().isoformat()
esc_pressed = False

def load_data():
    if not os.path.exists(KEYSTROKES_FILE):
        return {}
    with open(KEYSTROKES_FILE, 'r') as f:
        return yaml.safe_load(f)

def save_data(data):
    with open(KEYSTROKES_FILE, 'w') as f:
        yaml.dump(data, f)

def on_press(key):
    global keystrokes, current_date, esc_pressed

    # Check if date has changed and reset count if it has
    if datetime.date.today().isoformat() != current_date:
        current_date = datetime.date.today().isoformat()
        keystrokes = 0

    if key == Key.esc:
        esc_pressed = True
    elif esc_pressed and key == Key.delete:
        return False
    else:
        esc_pressed = False
        keystrokes += 1

def on_release(key):
    if key == Key.esc and not esc_pressed:
        return False

def graph_data(data):
    dates = list(data.keys())
    counts = list(data.values())

    plt.plot(dates, counts, marker='o')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.ylabel('Keystrokes')
    plt.title('Daily Keystrokes Count')
    plt.show()

def main():
    # Load existing data
    data = load_data()
    if current_date in data:
        global keystrokes
        keystrokes = data[current_date]

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    # Save updated data
    data[current_date] = keystrokes
    save_data(data)

    # Graph data
    graph_data(data)

if __name__ == '__main__':
    main()


