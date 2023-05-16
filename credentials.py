import tkinter as tk


def save_credentials():
    username = username_entry.get()
    password = password_entry.get()
    with open('/var/tmp/creds.txt', 'w') as f:
        f.write(f'{username}\n{password}')
    message_label.config(text="Credentials saved!")


root = tk.Tk()
root.title("Enter Credentials")

# Add a label for the username
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)

# Add an entry for the username
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Add a label for the password
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)

# Add an entry for the password
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Add a button to save the credentials
save_button = tk.Button(root, text="Save", command=save_credentials)
save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Add a label to display messages
message_label = tk.Label(root, text="")
message_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
