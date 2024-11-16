import socket

# Inicializon nje klient (UDP)
def start_client(server_host="ip", server_port=port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
