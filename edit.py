import os
import json
import subprocess
import pyperclip
from colorama import init, Fore, Style
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

def modify_config(url):
    if not os.path.isfile(file_path):
        print_message('config.json file not found in the script directory.', Fore.RED)
        return False

    with open(file_path, 'r') as file:
        data = json.load(file)

    if "items" not in data:
        print_message('"items" section not found in the JSON file.', Fore.RED)
        return False

    url = url.replace("https://www.roblox.com/catalog/", "").replace("https://web.roblox.com/catalog/", "").split("/")[0]
    data["items"] = [url]

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print_message('Items modified successfully!', Fore.GREEN)

    return True

# Starting message
print_message("Clipboard Monitor is active. Waiting for valid Roblox catalog link...", Fore.CYAN)

# Initial clipboard text
clipboard_text = ""

# Define the timer duration in seconds (10 minutes = 600 seconds)
timer_duration = 600

# Start the timer
start_time = time.time()

# Infinite loop
while True:
    # Check the clipboard contents
    new_clipboard_text = pyperclip.paste()

    if new_clipboard_text != clipboard_text:
        clipboard_text = new_clipboard_text

        if clipboard_text.startswith("https://www.roblox.com/catalog/") or clipboard_text.startswith("https://web.roblox.com/catalog/"):
            # Modify the config with the clipboard URL
            if modify_config(clipboard_text):
                try:
                    subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py')], shell=True)
                    print_message('main.py opened successfully!', Fore.YELLOW)
                    print_message("Clipboard Monitor is active. Waiting for valid Roblox catalog link...", Fore.CYAN)
                    pyperclip.copy("redacted")  # Set clipboard contents to "redacted"
                except Exception as e:
                    print_message(f'An error occurred while opening main.py: {str(e)}', Fore.RED)

    # Check if the timer has ended
    elapsed_time = time.time() - start_time
    if elapsed_time >= timer_duration:
        # Restart the program
        subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'edit.py')], shell=True)
        break

    # Wait for a short duration before checking clipboard again
    time.sleep(0.1)
