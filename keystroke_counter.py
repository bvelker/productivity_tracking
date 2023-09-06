import os, yaml
from pynput.keyboard import Key, Listener
import datetime
import matplotlib.pyplot as plt
import logging
from lines_added_github_api import GithubTracker
from dotenv import load_dotenv

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
    dates = sorted(data.keys())
    counts = [data[date]['keystrokes'] if isinstance(data[date], dict) else data[date] for date in dates]

    plt.plot(dates, counts, marker='o')
    plt.title('Keystrokes Over Time')
    plt.xlabel('Date')
    plt.ylabel('Keystrokes')
    plt.grid(True)
    plt.show()


def main():
    # Load existing data
    data = load_data()
    global keystrokes
    if current_date in data:
        keystrokes = data[current_date]['keystrokes']
    else:
        keystrokes = 0

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Save updated data
    data[current_date] = {
        'keystrokes': keystrokes,
    }
    
    # Load environment variables
    load_dotenv()
    username = 'bvelker'
    token = os.environ['GITHUB_TOKEN']
    tracker = GithubTracker(username, token)

    # Get GitHub commit data
    github_data = tracker.generate_yaml_ready_dict(datetime.datetime.now())
    data[current_date]['github_data'] = github_data

    save_data(data)

    # Graph data
    graph_data(data)


if __name__ == '__main__':
    main()
