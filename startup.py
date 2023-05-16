import os
import subprocess
import tkinter as tk

# Define a function to run the GUI file
def run_gui():
    gui_file_path = "etc/APP/GUI.py"
    if not os.path.isfile(gui_file_path):
        print(f"Error: GUI file '{gui_file_path}' does not exist.")
        return

    cmd = f"python {gui_file_path}"
    subprocess.Popen(cmd, shell=True)

# Create the main window
root = tk.Tk()

# Set the window to full screen
root.attributes('-fullscreen', True)

# Run the GUI file
run_gui()

# Run the main event loop
root.mainloop()
