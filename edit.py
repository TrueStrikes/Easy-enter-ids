import os
import json
import subprocess
import pyperclip
from colorama import init, Fore, Style
import time
from urllib.parse import urlparse
import re

# Initialize colorama
init()

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'config.json')
log_file_path = os.path.join(script_dir, 'log.json')

# Define the input prompt color
input_prompt_color = Fore.LIGHTBLUE_EX

def print_message(message, color):
    print(f"{color}{message}{Style.RESET_ALL}")

def modify_config(item_id):
    if not os.path.isfile(file_path):
        print_message('config.json file not found in the script directory.', Fore.RED)
        return False

    with open(file_path, 'r') as file:
        data = json.load(file)

    data["items"] = [item_id]

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print_message('Items modified successfully!', Fore.GREEN)

    return True

def update_log(log_file_path, item_id, item_name):
    with open(log_file_path, 'r+') as log_file:
        try:
            log_data = json.load(log_file)
        except json.JSONDecodeError:
            log_data = []

        if {"id": item_id, "name": item_name} not in log_data:
            log_data.append({"id": item_id, "name": item_name})
            log_file.seek(0)
            json.dump(log_data, log_file, indent=4)
            log_file.truncate()

def get_item_details(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    if len(path_parts) >= 3 and path_parts[2].isdigit():
        item_id = path_parts[2]
        item_name = path_parts[3] if len(path_parts) >= 4 else "Unknown"
        return item_id, item_name
    return None, None

def detect_11_digit_integer(clipboard_text):
    # Use regular expression to find 11-digit integers
    matches = re.findall(r'\b\d{11}\b', clipboard_text)
    return matches

def open_main_py():
    subprocess.Popen(['start', 'python', os.path.join(script_dir, 'main.py')], shell=True)

# Clear the console
os.system("cls" if os.name == "nt" else "clear")

# Starting message
print_message("Clipboard Monitor is active. Waiting for valid Roblox catalog link...", Fore.CYAN)

# Initial clipboard text
clipboard_text = ""

# Define the timer duration in seconds (1 hour = 3600 seconds)
timer_duration = 3600

# Start the timer
start_time = time.time()

# Infinite loop
while True:
    # Check the clipboard contents
    new_clipboard_text = pyperclip.paste()

    if new_clipboard_text != clipboard_text:
        clipboard_text = new_clipboard_text

        # Reset the flag at the beginning of each iteration
        main_py_opened = False

        # Detect Roblox catalog links
        if clipboard_text.startswith("https://www.roblox.com/catalog/") or clipboard_text.startswith("https://web.roblox.com/catalog/"):
            # Modify the config with the clipboard URL
            if modify_config(clipboard_text) and not main_py_opened:
                try:
                    open_main_py()
                    main_py_opened = True
                    print_message('main.py opened successfully!', Fore.GREEN)
                    pyperclip.copy("redacted")  # Set clipboard contents to "redacted"

                    # Extract and log the item ID and item name
                    item_id, item_name = get_item_details(clipboard_text)
                    if item_id:
                        update_log(log_file_path, item_id, item_name)

                    print_message("Clipboard Monitor is active. Waiting for valid Roblox catalog link...", Fore.CYAN)
                except Exception as e:
                    print_message(f'An error occurred while opening main.py: {str(e)}', Fore.RED)

        # Detect 11-digit integers and modify config if found
        detected_integers = detect_11_digit_integer(clipboard_text)
        if detected_integers:
            for item_id in detected_integers:
                if modify_config(item_id) and not main_py_opened:
                    main_py_opened = True
                    print_message(f'Item ID {item_id} detected and added to config.json.', Fore.YELLOW)
                    open_main_py()
                    pyperclip.copy("redacted")  # Set clipboard contents to "redacted"

    # Check if the timer has ended
    elapsed_time = time.time() - start_time
    if elapsed_time >= timer_duration:
        # Restart the program
        subprocess.Popen(['start', 'python', os.path.join(script_dir, 'edit.py')], shell=True)
        break

    # Wait for a short duration before checking clipboard again
    time.sleep(0.05)
