import os
import json
import subprocess
from colorama import init, Fore, Style
import clipboard
import time

# Initialize colorama
init()

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'config.json')

# Define the input prompt color
input_prompt_color = Fore.LIGHTBLUE_EX

def print_message(message, color):
    print(f"{color}{message}{Style.RESET_ALL}")

def modify_config():
    if not os.path.isfile(file_path):
        print_message('config.json file not found in the script directory.', Fore.RED)
        return False

    with open(file_path, 'r') as file:
        data = json.load(file)

    if "items" not in data:
        print_message('"items" section not found in the JSON file.', Fore.RED)
        return False

    print_message("Enter the URL/itemID (or 'exit' to quit):", input_prompt_color)
    url = input()

    if url.lower() == "exit":
        return False

    url = url.replace("https://www.roblox.com/catalog/", "").split("/")[0]
    data["items"] = [url]

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print_message('Items modified successfully!', Fore.GREEN)

    return True

def detect_clipboard_changes():
    print_message("Searching started!", Fore.YELLOW)

    last_detected_item = None

    while True:
        current_clipboard = clipboard.paste()

        # Check if clipboard content has changed
        if current_clipboard:
            url = current_clipboard.strip()
            if url.startswith("https://www.roblox.com/catalog/"):
                item_id = url.replace("https://www.roblox.com/catalog/", "").split("/")[0]

                if item_id != last_detected_item:  # Check if it's a new item
                    print("Detected Item ID:", item_id)
                    last_detected_item = item_id

                    try:
                        subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py')], shell=True)
                        print_message('main.py opened successfully!', Fore.YELLOW)
                    except Exception as e:
                        print_message(f'An error occurred while opening main.py: {str(e)}', Fore.RED)

        # Add a delay to avoid constant polling
        time.sleep(1)

# Call the function to detect clipboard changes
detect_clipboard_changes()

# Infinite loop
while modify_config():
    pass
