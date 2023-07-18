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

    processed_items = []  # List to store processed item IDs
    cooldown_duration = 5  # Cooldown period in seconds
    last_detection_time = 0  # Time of the last detection
    previous_clipboard = ""  # Previous clipboard content

    while True:
        current_clipboard = clipboard.paste()

        # Check if clipboard content has changed
        if current_clipboard != previous_clipboard:
            # Automatically enter detected item ID
            url = current_clipboard.strip()
            if url.startswith("https://www.roblox.com/catalog/"):
                item_id = url.replace("https://www.roblox.com/catalog/", "").split("/")[0]

                # Check if cooldown period has passed since the last detection
                current_time = time.time()
                if current_time - last_detection_time >= cooldown_duration:
                    if item_id not in processed_items:  # Check if item ID is new
                        print("Detected Item ID:", item_id)
                        processed_items.append(item_id)  # Add item ID to the processed list
                        # Automatically enter the item ID into the config file or perform desired actions

                        try:
                            subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py')], shell=True)
                            print_message('main.py opened successfully!', Fore.YELLOW)
                        except Exception as e:
                            print_message(f'An error occurred while opening main.py: {str(e)}', Fore.RED)

                    # Update the last detection time and previous clipboard
                    last_detection_time = current_time
                    previous_clipboard = current_clipboard

        # Add a delay to avoid constant polling
        time.sleep(1)

# Call the function to detect clipboard changes
detect_clipboard_changes()

# Infinite loop
while modify_config():
    pass
