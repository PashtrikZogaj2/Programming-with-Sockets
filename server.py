import os
import socket
import json
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Desktop/ggwp")  # Folder path to your ggwp folder
LOGGED_IN_USERS = {}  # Dictionary to store logged-in users {address: username}


def ensure_base_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)  # Creates the folder if it doesn't exist


def log_activity(message):
    """Print activity log to the terminal."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

def load_users():
    """Load user data from the JSON file."""
    with open("users.json", "r") as f:
        return json.load(f)["users"]


def authenticate(username, password, users):
    """Authenticate a user based on the JSON data."""
    return username in users and users[username]["password"] == password


def get_role(username, users):
    """Get the role of a user."""
    return users[username]["role"] if username in users else None


def handle_request(data, addr, server_socket, users):
    global LOGGED_IN_USERS
    # Split the command and arguments
    command, *args = data.decode("utf-8").split(" ", 1)

    if command == "login" and args:
        username, password = args[0].split(" ", 1)
        if authenticate(username, password, users):
            LOGGED_IN_USERS[addr] = username
            response = f"Logged in successfully as '{username}'."                 
            log_activity(f"{username} logged in from {addr}.")
        else:
            response = "Invalid username or password."
    elif addr in LOGGED_IN_USERS:
        username = LOGGED_IN_USERS[addr]
        role = get_role(username, users)

        if command == "list":
            files = os.listdir(BASE_DIR)
            response = "\n".join(files) if files else "No files found."
            log_activity(f"{username} executed 'list' command.")
        elif command == "read" and args:
            file_path = os.path.join(BASE_DIR, args[0])
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    response = f.read()
                log_activity(f"{username} read file '{args[0]}'.")
            else:
              response = "Invalid username or password."
    elif addr in LOGGED_IN_USERS:
        username = LOGGED_IN_USERS[addr]
        role = get_role(username, users)

        if command == "list":
            files = os.listdir(BASE_DIR)
            response = "\n".join(files) if files else "No files found."
            log_activity(f"{username} executed 'list' command.")
        elif command == "read" and args:
            file_path = os.path.join(BASE_DIR, args[0])
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    response = f.read()
                log_activity(f"{username} read file '{args[0]}'.")
            else:
                response = f"File '{args[0]}' not found."
                log_activity(f"{username} tried to read non-existent file '{args[0]}'.")
        elif command == "write" and args:
            if role == "admin":
                file_name, content = args[0].split(" ", 1)
                file_path = os.path.join(BASE_DIR, file_name)
                with open(file_path, "w") as f:
                    f.write(content)
                response = f"File '{file_name}' written successfully."
                log_activity(f"{username} wrote to file '{file_name}'.")
            else:
                response = "Permission denied. Only admins can write files."
                log_activity(f"{username} attempted to write file '{args[0]}' without permission.")
        elif command == "delete" and args:
            if role == "admin":
                file_path = os.path.join(BASE_DIR, args[0])
                if os.path.exists(file_path):
                    os.remove(file_path)
                    response = f"File '{args[0]}' deleted successfully."
                    log_activity(f"{username} deleted file '{args[0]}'.")
                else:
                    response = f"File '{args[0]}' not found."
                    log_activity(f"{username} attempted to delete non-existent file '{args[0]}'.")
            else:
                response = "Permission denied. Only admins can delete files."
                log_activity(f"{username} attempted to delete file '{args[0]}' without permission.")
        elif command == "send" and args:
            recipient, message = args[0].split(" ", 1)
            recipient_addr = next((addr for addr, user in LOGGED_IN_USERS.items() if user == recipient), None)
            if recipient_addr:
                server_socket.sendto(f"Message from {username}: {message}".encode("utf-8"), recipient_addr)
                response = f"Message sent to {recipient}."
                log_activity(f"{username} sent a message to {recipient}: {message}")
            else:
                response = f"User '{recipient}' is not logged in."
                log_activity(f"{username} attempted to send a message to offline user '{recipient}'.")
        else:
            response = f"Unknown command: {command}"
            log_activity(f"{username} issued an unknown command: {command}")
    else:
     response = "You must log in first using 'login <username> <password>'."
    log_activity(f"Unauthorized attempt to execute '{command}' from {addr}.")

    server_socket.sendto(response.encode("utf-8"), addr)


def start_server(host="0.0.0.0", port=24525):
    ensure_base_dir()
    users = load_users()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Server started on {host}:{port}. Waiting for commands...")
    log_activity("Server started.")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            handle_request(data, addr, server_socket, users)
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            log_activity("Server shutting down.")
            break

    server_socket.close()


if _name_ == "_main_":
  start_server()





