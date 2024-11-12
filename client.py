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
        
# Check if the user wants to exit
        if message.lower() == 'exit':
            print("Exiting the client.")
            break
        
        # Send the message to the server
        client_socket.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))
        print(f"Message sent to {SERVER_IP}:{SERVER_PORT}")
        
        # Receive and print the response from the server
        response, server_address = client_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Response from server: {response.decode('utf-8')}")
        
finally:
    # Close the client socket when done
    client_socket.close()
    print("Client socket closed.")