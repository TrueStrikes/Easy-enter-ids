import os
import json
import subprocess
from colorama import init, Fore, Style

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

    try:
        subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py')], shell=True)
        print_message('main.py opened successfully!', Fore.YELLOW)
    except Exception as e:
        print_message(f'An error occurred while opening main.py: {str(e)}', Fore.RED)

    return True

# Infinite loop
while modify_config():
    pass
