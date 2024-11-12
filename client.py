import socket

# Define the server's IP address and port
SERVER_IP = '192.168.0.138'  # Replace with the server's actual IP address
SERVER_PORT = 12345      # Replace with the actual server port

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Prompt the user to input a message
        message = input("Enter a message to send to the server (or type 'exit' to quit): ")
        
