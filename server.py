import os
import socket

BASE_DIR = os.path.expanduser("~/Desktop/ggwp")  # Rruga e folderit ggwp | Path-i, Lokacioni

# Krijon folderin nese nuk ekziston
def ensure_base_dir():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

# Menaxhon kerkesat nga klienti
def handle_request(data, addr, server_socket):
    # Ndaj komanden dhe argumentet
    command, *args = data.decode("utf-8").split(" ", 1)

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
