import os
from tkinter import Tk, Listbox, Button, END, ttk
from colorama import Fore, Style
import subprocess
import json

def open_main(item):
    print(f"{Fore.GREEN}Opening main.py with item: {item}{Style.RESET_ALL}")
    try:
        subprocess.Popen(['cmd', '/c', 'start', 'python', 'main.py'])
    except Exception as e:
        print(f'An error occurred while opening main.py: {str(e)}')

def main():
    # Read the log file
    with open('log.txt', 'r') as file:
        log_data = file.readlines()

    # Create the GUI window
    root = Tk()
    root.title("Item Selector")
    root.geometry("400x400")
    root.configure(bg='black')

    # Create a Listbox to display the items
    listbox = Listbox(root, bg='black', fg='yellow', font=("Arial", 12))
    listbox.pack(fill='both', expand=True, padx=10, pady=10)

    # Insert the items into the Listbox
    for line in log_data:
        item_id, item_name = line.strip().split(',')
        listbox.insert(END, f"ID: {item_id} - Name: {item_name}")
        listbox.insert(END, '-' * 40)

    # Function to handle item selection
    def select_item(event):
        selected_item = listbox.get(listbox.curselection())
        item_id = selected_item.split(':')[1].strip().split()[0]
        item_name = selected_item.split('- Name:')[1].strip()
        open_main(item_id)
        modify_config(item_id)
        root.destroy()

    # Bind the double click event to the item selection function
    listbox.bind("<Double-Button-1>", select_item)

    # Start the GUI event loop
    root.mainloop()

def modify_config(item_id):
    # Modify the contents of the config.json file with the selected item ID
    file_path = 'config.json'
    if os.path.isfile(file_path):
        with open(file_path, 'r+') as file:
            data = json.load(file)
            data['items'] = [item_id]
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            print(f"{Fore.MAGENTA}Config file modified successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Config file not found!{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
