import os
import json
import subprocess
from tkinter import *
from tkinter import messagebox

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, 'log.json')

def load_logs():
    if os.path.isfile(log_file_path):
        with open(log_file_path, 'r') as log_file:
            try:
                log_data = json.load(log_file)
            except json.JSONDecodeError:
                log_data = []
    else:
        log_data = []

    return log_data

def create_gui():
    def open_item():
        selected_item = listbox.get(ANCHOR)
        item = json.loads(selected_item)
        item_id = item["id"]
        subprocess.Popen(['cmd', '/c', 'start', 'python', 'main.py', item_id], shell=True)

    def delete_item():
        selected_item = listbox.get(ANCHOR)
        item = json.loads(selected_item)
        item_id = item["id"]

        log_data = load_logs()
        log_data = [item for item in log_data if item["id"] != item_id]

        with open(log_file_path, 'w') as log_file:
            json.dump(log_data, log_file, indent=4)

        update_listbox()
        messagebox.showinfo("Success", "Item deleted successfully.")

    def refresh():
        log_data = load_logs()
        update_listbox()

    def update_listbox():
        listbox.delete(0, END)
        log_data = load_logs()
        for item in log_data:
            item_name = item["name"]
            listbox.insert(END, item_name)

    # Create the main window
    root = Tk()
    root.title("Logged Items")
    root.configure(bg="black")

    # Create the listbox
    listbox = Listbox(root, font=("Arial", 12), bg="black", fg="yellow")
    listbox.pack(pady=10)

    # Create a scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Set the scrollbar to the listbox
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Add buttons
    open_button = Button(root, text="Open Item", command=open_item)
    open_button.pack(pady=5)

    delete_button = Button(root, text="Delete Item", command=delete_item)
    delete_button.pack(pady=5)

    refresh_button = Button(root, text="Refresh", command=refresh)
    refresh_button.pack(pady=5)

    # Load the initial items in the listbox
    update_listbox()

    # Start the GUI main loop
    root.mainloop()

# Call the create_gui function to start the application
create_gui()
