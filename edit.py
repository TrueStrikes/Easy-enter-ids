import os
import json
import subprocess
import pyperclip
import time
from colorama import init, Fore, Style
from urllib.parse import urlparse

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

def modify_config(url):
    if not os.path.isfile(file_path):
        print_message('config.json file not found in the script directory.', Fore.RED)
        return False

    with open(file_path, 'r') as file:
        data = json.load(file)

    if "items" not in data:
        print_message('"items" section not found in the JSON file.', Fore.RED)
        return False

    url = url.replace("https://www.roblox.com/catalog/", "").replace("https://web.roblox.com/catalog/", "").replace("roblox.com/catalog/", "").split("/")[0]
    data["items"] = [url]

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

def is_valid_11_digit_number(text):
    return text.isdigit() and len(text) == 11

def is_valid_roblox_catalog_link(url):
    return (
        url.startswith("https://www.roblox.com/catalog/") or 
        url.startswith("https://web.roblox.com/catalog/") or
        url.startswith("www.roblox.com/catalog/") or
        url.startswith("roblox.com/catalog/")
    )

# Clear the console
os.system("cls" if os.name == "nt" else "clear")

# Starting message
print_message("Clipboard Monitor is active. Waiting for valid Roblox catalog link...", Fore.CYAN)

# Initialize clipboard_text variable
clipboard_text = ""

# Infinite loop
while True:
    # Check the clipboard contents
    new_clipboard_text = pyperclip.paste()

    if new_clipboard_text != clipboard_text:
        clipboard_text = new_clipboard_text

        if is_valid_roblox_catalog_link(clipboard_text) or is_valid_11_digit_number(clipboard_text):
            # Modify the config with the clipboard URL or 11-digit integer
            if modify_config(clipboard_text):
                try:
                    subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py')], shell=True)
                    print_message('main.py opened successfully!', Fore.GREEN)
                    pyperclip.copy("redacted")  # Set clipboard contents to "redacted"

                    # Extract and log the item ID and item name
                    item_id, item_name = get_item_details(clipboard_text)
                    if item_id:
                        update_log(log_file_path, item_id, item_name)

                    print_message("Clipboard Monitor is active. Waiting for valid Roblox catalog link...", Fore.CYAN)
                except Exception as e:
                    print_message(f'An error occurred while opening main.py: {str(e)}', Fore.RED)

    # Wait for a short duration before checking clipboard again
    time.sleep(0.05)
