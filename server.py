import os
import socket

BASE_DIR = os.path.expanduser("~/Desktop/ggwp")  # Rruga e folderit ggwp | Path-i, Lokacioni
LOGGED_IN_USERS = {}  # Dictionary to store logged-in users {address: username}



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


# Krijon folderin nese nuk ekziston
def ensure_base_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

# Menaxhon kerkesat nga klienti
def handle_request(data, addr, server_socket):
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

        # Operacionet mbi fajllet
        if command == "list":
            files = os.listdir(BASE_DIR)  # Liston fajllat ne folder
            response = "\n".join(files) if files else "No files found."
        elif command == "read" and args:
            file_path = os.path.join(BASE_DIR, args[0])  # Rruga e follderit ( fajllit, Path-i )
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    response = f.read()  # Lexon permbajtjen e skedarit
            else:
                response = f"File '{args[0]}' not found."  # Fajlli nuk u gjet
        elif command == "write" and args:
            file_name, content = args[0].split(" ", 1)
            file_path = os.path.join(BASE_DIR, file_name)
            with open(file_path, "w") as f:
                f.write(content)
            response = f"File '{file_name}' written successfully."
        elif command == "delete" and args:
            file_path = os.path.join(BASE_DIR, args[0])
            if os.path.exists(file_path):
                os.remove(file_path)
                response = f"File '{args[0]}' deleted successfully."
            else:
                response = f"File '{args[0]}' not found."
        # Chat messages (anything that's not a file operation)
        else:
            response = f"Chat Message: {data.decode('utf-8')}"
            
            server_socket.sendto(response.encode("utf-8"), addr)

            def start_server(host="0.0.0.0", port=port):
            ensure_base_dir()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Server started on {host}:{port}. Waiting for commands...")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            handle_request(data, addr, server_socket)
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break

    server_socket.close()

if _name_ == "_main_":
    start_server()

