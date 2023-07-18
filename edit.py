import os
import json
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init()

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path to config.json
file_path = os.path.join(script_dir, 'config.json')

# Define the input prompt color
input_prompt_color = Fore.LIGHTBLUE_EX

# Prompt message for item input
prompt_message = f"{input_prompt_color}Enter the URL/itemID (or 'exit' to quit): {Style.RESET_ALL}"

# Check if config.json exists
if not os.path.isfile(file_path):
    print('config.json file not found in the script directory.')
    exit()

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Check if "items" section exists
if "items" not in data:
    print('"items" section not found in the JSON file.')
    exit()

# Infinite loop
while True:
    print(prompt_message, end="")
    url = input()

    if url.lower() == "exit":
        break

    url = url.replace("https://www.roblox.com/catalog/", "").split("/")[0]
    data["items"] = [url]

    # Save the modified JSON data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    # Glow effect
    print(f"{Fore.GREEN}{Style.BRIGHT}Items modified successfully!{Style.RESET_ALL}")

    try:
        main_file_path = os.path.join(script_dir, 'main.py')
        subprocess.Popen(['cmd', '/c', 'start', 'python', main_file_path], shell=True)
        print(f"{Fore.YELLOW}main.py opened successfully!{Style.RESET_ALL}")
    except Exception as e:
        print('An error occurred while opening main.py:', str(e))
