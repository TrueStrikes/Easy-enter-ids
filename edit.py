import os
import json
import subprocess
from colorama import init, Fore, Style
import pyperclip
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
    previous_clipboard = ""

    while True:
        current_clipboard = pyperclip.paste()

        # Check if clipboard content has changed
        if current_clipboard != previous_clipboard:
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

        # Prompt to reopen main.py with the last detected item ID
        if last_detected_item is not None:
            print_message("Press 'Enter' to reopen main.py with the last detected item ID:", input_prompt_color)
            input()  # Wait for user to press Enter

            try:
                subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py'), last_detected_item], shell=True)
                print_message('main.py reopened successfully with the last detected item ID!', Fore.YELLOW)

            except Exception as e:
                print_message(f'An error occurred while reopening main.py: {str(e)}', Fore.RED)
            last_detected_item = None  # Reset last detected item ID

        previous_clipboard = current_clipboard  # Update previous clipboard content

        # Add a delay to avoid constant polling
        time.sleep(1)

# Call the function to detect clipboard changes
detect_clipboard_changes()

# Infinite loop
while modify_config():
    pass
