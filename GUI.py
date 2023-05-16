import os
import subprocess
import tkinter as tk
import paramiko

# Define functions to run different scripts
def run_script(script_path):
    if not os.path.isfile(script_path):
        print(f"Error: script '{script_path}' does not exist.")
        return
    cmd = f"python {script_path}"
    subprocess.Popen(cmd, shell=True)

#Default creds to Adtran standards
creds_file = 'creds.txt'
with open(creds_file, 'w') as f:
   f.write('ADMIN\nPASSWORD\n')

def connect_to_server():
    try:
       with open(creds_file, 'r') as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
       # Create an SSH client object
       client = paramiko.SSHClient()   
       # Automatically add the server's host key
       client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
       # Connect to the server
       client.connect('10.100.2.32', username=username, password=password)   
       # Run the 'en' command
       stdin, stdout, stderr = client.exec_command('en')
       print(stdout.read().decode())   
       # Run the 'show running-config | include ip file-server default host' command
       stdin, stdout, stderr = client.exec_command('show running-config | include ip file-server default host')
       output = stdout.read().decode()   
       # Store the output in a temporary file
       with open('/tmp/output.txt', 'w') as f:
           f.write(output)   
       # Run the 'set ip file-server default host 10.100.2.20' command
       stdin, stdout, stderr = client.exec_command('set ip file-server default host 10.100.2.20')
       print(stdout.read().decode())   
       # Exit the session
       stdin, stdout, stderr = client.exec_command('exit')
       print(stdout.read().decode())   
       # Close the SSH connection
       client.close()

       print("Connected to server.")
    except Exception as e:
        print(f"Error: {str(e)}")

def disconnect_from_server():
    try:
        with open(creds_file, 'r') as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()

        # Create an SSH client object
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        client.connect('10.100.2.20', username=username, password=password)

        # Run the 'en' command
        stdin, stdout, stderr = client.exec_command('en')
        print(stdout.read().decode())

        # Read the value of the ip file-server default host setting from the output file
        with open('output.txt', 'r') as f:
            output = f.read().strip()

        # Set the ip file-server default host setting
        stdin, stdout, stderr = client.exec_command(f'ip file-server default host {output}')
        print(stdout.read().decode())

        # Exit the session
        stdin, stdout, stderr = client.exec_command('exit')
        print(stdout.read().decode())

        # Close the SSH connection
        client.close()

        print("Disconnected from server.")
    except Exception as e:
        print(f"Error: {str(e)}")

def apply_custom_conf_file():
    try:
        with open(creds_file, 'r') as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()

        # Create an SSH client object
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        server_ip = "10.100.2.32"
        try:
            client.connect(server_ip, username=username, password=password)
        except Exception as e:
            print(f"Failed to connect to {server_ip}: {e}")
            exit()

        # Prompt the user to locate the configuration file
        file_path = fd.askopenfilename(title="Select Configuration File")

        # Read the contents of the configuration file
        if not os.path.isfile(file_path):
            print(f"Error: file '{file_path}' does not exist.")
            exit()

        with open(file_path, 'r') as f:
            conf_data = f.read()

        # Prompt the user for confirmation
        confirmation = input("Are you sure you want to apply the configuration file? (y/n) ")
        if confirmation.lower() != "y":
            print("Configuration file not applied.")
            exit()

        # Apply the configuration file line by line
        stdin, stdout, stderr = client.exec_command('en')
        print(stdout.read().decode())

        for line in conf_data.splitlines():
            stdin, stdout, stderr = client.exec_command(line)
            print(stdout.read().decode())

        # Exit the session
        stdin, stdout, stderr = client.exec_command('exit')
        print(stdout.read().decode())

        # Close the SSH connection
        client.close()

        print(f"Configuration file '{file_path}' applied.")
    except Exception as e:
        print(f"Error: {str(e)}")

def apply_default_conf_file():
    try:
        with open(creds_file, 'r') as f:
            lines = f.readlines()
            username = lines[0].strip()
            password = lines[1].strip()

        # Create an SSH client object
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        server_ip = "10.100.2.32"
        try:
            client.connect(server_ip, username=username, password=password)
        except Exception as e:
            print(f"Failed to connect to {server_ip}: {e}")
            exit()

        # Read the contents of the configuration file
        conf_file_path = "/etc/TA5k/default.txt"
        if not os.path.isfile(conf_file_path):
            print(f"Error: file '{conf_file_path}' does not exist.")
            exit()

        with open(conf_file_path, 'r') as f:
            conf_data = f.read()

        # Prompt the user for confirmation
        confirmation = input("Are you sure you want to apply the configuration file? (y/n) ")
        if confirmation.lower() != "y":
            print("Configuration file not applied.")
            exit()

        # Apply the configuration file line by line
        stdin, stdout, stderr = client.exec_command('en')
        print(stdout.read().decode())

        for line in conf_data.splitlines():
            stdin, stdout, stderr = client.exec_command(line)
            print(stdout.read().decode())

        # Exit the session
        stdin, stdout, stderr = client.exec_command('exit')
        print(stdout.read().decode())

        # Close the SSH connection
        client.close()

        print("Default configuration file applied.")
    except Exception as e:
        print(f"Error: {str(e)}")

def enter_credentials():
    def save_credentials():
        username = username_entry.get()
        password = password_entry.get()
        with open(creds_file, 'w') as f:
            f.write(f'{username}\n{password}')
        message_label.config(text="Credentials saved!")

    credentials_window = tk.Toplevel()
    credentials_window.title("Enter Credentials")

    # Add a label for the username
    username_label = tk.Label(credentials_window, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    # Add an entry for the username
    username_entry = tk.Entry(credentials_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    # Add a label for the password
    password_label = tk.Label(credentials_window, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    # Add an entry for the password
    password_entry = tk.Entry(credentials_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add a button to save the credentials
    save_button = tk.Button(credentials_window, text="Save", command=save_credentials)
    save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Add a label to display messages
    message_label = tk.Label(credentials_window, text="")
    message_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    credentials_window.mainloop()


# Create the main window
root = tk.Tk()
root.title("5K Rescue")

# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Add a "Settings" menu item to the menu bar
settings_menu = tk.Menu(menubar)
menubar.add_cascade(label="Settings", menu=settings_menu)

# Add a menu item for the settings page
def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Settings")

settings_menu.add_command(label="Settings", command=open_settings)

# Set window size and center it on the screen
window_width = 300
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set window icon
root.iconbitmap("Capture.ico")

# Set window background color
root.config(bg="#FFFFFF")

# Create title label
title_label = tk.Label(root, text="My 5K Rescue", font=("Arial", 20), bg="#FFFFFF")
title_label.pack(pady=10)

# Create the buttons
button_creds = tk.Button(root, text="Enter Credentials", font=("Arial", 14), command=enter_credentials)
button_connect = tk.Button(root, text="Connect to Server", font=("Arial", 14), command=connect_to_server)
button_apply_conf = tk.Button(root, text="Disconnect From Server", font=("Arial", 14), command=disconnect_from_server)
button_reverse_conf = tk.Button(root, text="Load Generated Config", font=("Arial", 14), command=apply_custom_conf_file)
button_apply_default_conf = tk.Button(root, text="Load Default Config", font=("Arial", 14), command=apply_default_conf_file)

# Set button colors
button_creds.config(bg="#F5A623", fg="#FFFFFF", activebackground="#FFC863")
button_connect.config(bg="#F5A623", fg="#FFFFFF", activebackground="#FFC863")
button_apply_conf.config(bg="#007AFF", fg="#FFFFFF", activebackground="#66B3FF")
button_reverse_conf.config(bg="#FF2D55", fg="#FFFFFF", activebackground="#FF6384")
button_apply_default_conf.config(bg="#4CD964", fg="#FFFFFF", activebackground="#5BE65B")

# Pack the buttons into the window
button_creds.pack(ipadx=20, pady=10)
button_connect.pack(ipadx=20, pady=10)
button_apply_conf.pack(ipadx=20, pady=10)
button_reverse_conf.pack(ipadx=20, pady=10)
button_apply_default_conf.pack(ipadx=20, pady=10)

# Run the main event loop
root.mainloop()