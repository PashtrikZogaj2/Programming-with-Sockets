import socket

def start_client(server_host="192.168.1.8", server_port=24525):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Connected to server at {server_host}:{server_port}.")
    
    # Login
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        client_socket.sendto(f"login {username} {password}".encode("utf-8"), (server_host, server_port))
        response, _ = client_socket.recvfrom(1024)
        print(response.decode("utf-8"))
        if "Logged in successfully" in response.decode("utf-8"):
            break

    print("Available commands:")
    print("  list                     - List files")
    print("  read <filename>          - Read a file")
    print("  write <filename> <text>  - Write text to a file (admin only)")
    print("  delete <filename>        - Delete a file (admin only)")
    print("  send <username> <message> - Send a message to another user")
    print("  exit                     - Exit the chat")

    while True:
        try:
            message = input("> ")
            if message.lower() == "exit":
                print("Exiting chat.")
                break
            client_socket.sendto(message.encode("utf-8"), (server_host, server_port))
            response, _ = client_socket.recvfrom(1024)
            print(response.decode("utf-8"))
        except KeyboardInterrupt:
            print("\nExiting client.")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()
