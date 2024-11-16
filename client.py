import socket

# Inicializon nje klient (UDP)
def start_client(server_host="ip", server_port=port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Connected to server at {server_host}:{server_port}.")
    print("Available commands:")
    print("  list                     - List files")
    print("  read <filename>          - Read a file")
    print("  write <filename> <text>  - Write text to a file")
    print("  delete <filename>        - Delete a file")
    print("  <text>                   - Send a chat message")
    print("  exit                     - Exit the chat")

    while True:
        try:
            # Read user input
            message = input("> ")

            if message.lower() == "exit":
                print("Exiting chat.")
                break

            # Send the message to the server
