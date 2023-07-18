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

# Infinite loop
while True:
    # Check if config.json exists
    if os.path.isfile(file_path):
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Search for the "items" section
        if "items" in data:
            # Prompt for item input
            print(f"{input_prompt_color}Enter the URL/itemID (or 'exit' to quit): {Style.RESET_ALL}", end="")
            url = input()

            if url.lower() == "exit":
                break  # Exit the loop

            # Remove unnecessary parts from the URL
            url = url.replace("https://www.roblox.com/catalog/", "")
            url = url.split("/")[0]  # Remove anything after the first slash

            # Modify the contents of the "items" list with the cleaned URL
            data["items"] = [url]

            # Save the modified JSON data back to the file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            # Glow effect
            print(f"{Fore.GREEN}{Style.BRIGHT}Items modified successfully!{Style.RESET_ALL}")

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
