import paramiko

# Prompt the user for their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Create an SSH client object
client = paramiko.SSHClient()

# Automatically add the server's host key
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the shelf
client.connect('10.100.2.32', username=username, password=password)

# Run the 'en' command
stdin, stdout, stderr = client.exec_command('en')
print(stdout.read().decode())

# Read the value of the ip file-server default host setting from the output file
with open('/tmp/output.txt', 'r') as f:
    output = f.read().strip()

# Set the ip file-server default host setting
stdin, stdout, stderr = client.exec_command(f'ip file-server default host {output}')
print(stdout.read().decode())

# Exit the session
stdin, stdout, stderr = client.exec_command('exit')
print(stdout.read().decode())

# Close the SSH connection
client.close()