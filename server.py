import os
import socket
import json
from datetime import datetime

BASE_DIR = os.path.expanduser("~/Desktop/ggwp")  # Vendi ku do te ruhen fajlat
LOGGED_IN_USERS = {}  #  Ruajtja e përdoruesve të kyçur {address: username}


def ensure_base_dir(): #Mu siguru se ekziston fajlli ne /Desktop/ggwp
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)  # Krijon te re, nese nuk ekziston


def log_activity(message): #Regjistron aktivitetet në terminal me datë dhe kohë
    """Regjistron aktivitetin në terminal."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")


def load_users():
    """Ngarkon të dhënat e përdoruesve nga .JSON files """
    with open("users.json", "r") as f:
        return json.load(f)["users"]


def authenticate(username, password, users):
    """Autentifikon përdoruesin duke krahasuar të dhënat nga JSON."""
    return username in users and users[username]["password"] == password


def get_role(username, users):
    """Kthen rolin e përdoruesit nga të dhënat JSON."""
    return users[username]["role"] if username in users else None

# Perpunon komandat e marra nga klientet
def handle_request(data, addr, server_socket, users):
    global LOGGED_IN_USERS
    # Ndajmë komandën dhe argumentet
    command, *args = data.decode("utf-8").split(" ", 1)

    if command == "login" and args:
        username, password = args[0].split(" ", 1)
        if authenticate(username, password, users):
            LOGGED_IN_USERS[addr] = username
            response = f"U kyçët me sukses si '{username}'."
            log_activity(f"{username} u kyç nga {addr}.")
        else:
            response = "Emri i përdoruesit ose fjalëkalimi janë të pasaktë."
    elif addr in LOGGED_IN_USERS:
        username = LOGGED_IN_USERS[addr]
        role = get_role(username, users)

        if command == "list":
            files = os.listdir(BASE_DIR)
            response = "\n".join(files) if files else "Nuk u gjet asnjë file."
            log_activity(f"{username} ekzekutoi komandën 'list' .")
        elif command == "read" and args:
            file_path = os.path.join(BASE_DIR, args[0])
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    response = f.read()
                log_activity(f"{username} lexoi file '{args[0]}'.")
            else:
                response = f"File '{args[0]}' nuk ekziston."
                log_activity(f"{username} tentoi të lexonte nje file qe nuk ekziston '{args[0]}'.")
        elif command == "write" and args:
            if role == "admin":
                file_name, content = args[0].split(" ", 1)
                file_path = os.path.join(BASE_DIR, file_name)
                with open(file_path, "w") as f:
                    f.write(content)
                response = f"File '{file_name}' u shkrua me sukses."
                log_activity(f"{username} shkroi tek file '{file_name}'.")
            else:
                response = "Leje e refuzuar. Vetëm adminët mund të shkruajnë files."
                log_activity(f"{username} tentoi te shkruaj nje file '{args[0]}' pa leje.")
        elif command == "delete" and args:
            if role == "admin":
                file_path = os.path.join(BASE_DIR, args[0])
                if os.path.exists(file_path):
                    os.remove(file_path)
                    response = f"File '{args[0]}' u fshi me sukses."
                    log_activity(f"{username} fshiu file '{args[0]}'.")
                else:
                    response = f"File '{args[0]}' nuk ekziston."
                    log_activity(f"{username} tentoi të fshinte nje file qe nuk ekziston'{args[0]}'.")
            else:
                response = "Leje e refuzuar. Vetëm adminët mund të fshijnë files."
                log_activity(f"{username} tentoi te fshinte file '{args[0]}' pa leje.")
        elif command == "send" and args:
            recipient, message = args[0].split(" ", 1)
            recipient_addr = next((addr for addr, user in LOGGED_IN_USERS.items() if user == recipient), None)
            if recipient_addr:
                server_socket.sendto(f"Mesazh nga {username}: {message}".encode("utf-8"), recipient_addr)
                response = f"Mesazhi u dërgua te {recipient}."
                log_activity(f"{username} dërgoi mesazh te {recipient}: {message}")
            else:
                response = f"Përdoruesi '{recipient}' nuk është i kyçur."
                log_activity(f"{username} u përpoq të dërgonte një mesazh te përdoruesi jashtë linje '{recipient}'.")
        else:
            response = f"Komandë e panjohur: {command}"
            log_activity(f"{username} shkruajti një komandë të panjohur: {command}")
    else:
        response = "Duhet të kyçeni së pari duke përdorur 'login <username> <password>'."
        log_activity(f"Tentim i paautorizuar për të ekzekutuar '{command}' nga {addr}.")

    server_socket.sendto(response.encode("utf-8"), addr)


def start_server(host="0.0.0.0", port=24525):
    ensure_base_dir()
    users = load_users()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Serveri u startua në {host}:{port}. Duke pritur komanda...")
    log_activity("Server u startua.")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            handle_request(data, addr, server_socket, users)
        except KeyboardInterrupt:
            print("\nServeri po mbyllet.")
            log_activity("Serveri po mbyllet.")
            break

    server_socket.close()


if __name__ == "__main__":
    start_server()
