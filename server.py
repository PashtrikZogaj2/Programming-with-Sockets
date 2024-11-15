import os
import socket

BASE_DIR = os.path.expanduser("~/Desktop/ggwp")  # Folder path to your ggwp folder

def ensure_base_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)  # Creates the folder if it doesn't exist

def handle_request(data, addr, server_socket):
    # Split the command and arguments
    command, *args = data.decode("utf-8").split(" ", 1)

    # File operations
    if command == "list":
        files = os.listdir(BASE_DIR)
        response = "\n".join(files) if files else "No files found."
    elif command == "read" and args:
        file_path = os.path.join(BASE_DIR, args[0])
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                response = f.read()
        else:
            response = f"File '{args[0]}' not found."