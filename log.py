import os
import json
import subprocess
import pyperclip
from colorama import init, Fore, Style
import time
from tkinter import *

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

    url = url.replace("https://www.roblox.com/catalog/", "").replace("https://web.roblox.com/catalog/", "").split("/")[0]
    data["items"] = [url]

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print_message('Items modified successfully!', Fore.GREEN)

    return True

def update_log(log_file_path, item_id, item_name):
    log_data = load_logs()

    if {"id": item_id, "name": item_name} not in log_data:
        log_data.append({"id": item_id, "name": item_name})
        save_logs(log_data)

def load_logs():
    if os.path.isfile(log_file_path):
        with open(log_file_path, 'r') as log_file:
            try:
                log_data = json.load(log_file)
                return log_data
            except json.JSONDecodeError:
                print_message("Invalid log file format. Creating a new log file.", Fore.YELLOW)
    return []

def save_logs(log_data):
    with open(log_file_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

def create_gui():
    logs = load_logs()

    root = Tk()
    root.title("Logged Items")
    root.configure(background="black")

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(root, width=50, height=20, font=("Courier New", 12), bg="black", fg="yellow", selectbackground="black", selectforeground="yellow")
    listbox.pack(side=LEFT, fill=BOTH)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    for item in logs:
        listbox.insert(END, item["name"])

    def open_item():
        selected_item = listbox.get(listbox.curselection())
        item = next((item for item in logs if item["name"] == selected_item), None)
        if item:
            item_id = item["id"]
            subprocess.Popen(['cmd', '/c', 'start', 'python', os.path.join(script_dir, 'main.py'), item_id], shell=True)

    def delete_item():
        selected_item = listbox.get(listbox.curselection())
        item = next((item for item in logs if item["name"] == selected_item), None)
        if item:
            logs.remove(item)
            save_logs(logs)
            refresh_list()

    def refresh_list():
        listbox.delete(0, END)
        for item in logs:
            listbox.insert(END, item["name"])

    open_button = Button(root, text="Open", width=10, command=open_item)
    open_button.pack(side=LEFT, padx=5, pady=10)

    delete_button = Button(root, text="Delete", width=10, command=delete_item)
    delete_button.pack(side=LEFT, padx=5, pady=10)

    refresh_button = Button(root, text="Refresh", width=10, command=refresh_list)
    refresh_button.pack(side=LEFT, padx=5, pady=10)

    root.mainloop()

create_gui()
