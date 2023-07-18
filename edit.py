import os
import json
import subprocess
import sys
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path to config.json
file_path = os.path.join(script_dir, 'config.json')

# Check if config.json exists
if os.path.isfile(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Search for the "items" section
    if "items" in data:
        # Get the item from the command-line argument
        if len(sys.argv) > 1:
            item = sys.argv[1]
        else:
            print('Please provide the item as a command-line argument.')
            sys.exit(1)

        # Modify the contents of the "items" list
        data["items"] = [item]

        # Save the modified JSON data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Glow effect
        print(f"{Fore.GREEN}{Style.BRIGHT}Items modified successfully!{Style.RESET_ALL}")
        time.sleep(1)  # Pause for 2 seconds

        try:
            # Execute main.py in a separate command prompt window
            main_file_path = os.path.join(script_dir, 'main.py')
            subprocess.Popen(['cmd', '/c', 'start', 'python', main_file_path], shell=True)
            print(f"{Fore.YELLOW}main.py opened successfully!{Style.RESET_ALL}")
        except Exception as e:
            print('An error occurred while opening main.py:', str(e))
    else:
        print('"items" section not found in the JSON file.')
else:
    print('config.json file not found in the script directory.')
