import os
import paramiko

# Prompt the user for confirmation
confirmation = input("Are you sure you want to apply the configuration file? (y/n) ")
if confirmation.lower() != "y":
    print("Configuration file not applied.")
    exit()

# Prompt the user for their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

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