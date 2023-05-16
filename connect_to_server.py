import paramiko

# Prompt the user for their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

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
