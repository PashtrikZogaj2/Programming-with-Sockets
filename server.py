import socket

# Define the server's IP address and port
IP_ADDRESS = ''  # Replace with the server's actual IP address
PORT = 12345  # Replace with any available port number

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port
server_socket.bind((IP_ADDRESS, PORT))
print(f"UDP server up and listening on {IP_ADDRESS}:{PORT}")

# Prompt the server user to input the IP and port for write access
write_ip = input("Enter the IP address of the client to grant write access: ")
write_port = int(input("Enter the port number of the client to grant write access: "))
WRITE_PRIVILEGE_CLIENT = (write_ip, write_port)
