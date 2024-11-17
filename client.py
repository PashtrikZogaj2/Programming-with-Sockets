import socket

def start_client(server_host="192.168.1.8", server_port=24525):
    """
    Nis klientin UDP për të komunikuar me serverin.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Lidhur me serverin në {server_host}:{server_port}.")
    
    # Login
    while True:
        username = input("Shkruaj emrin e përdoruesit: ")
        password = input("Shkruaj fjalëkalimin: ")
        client_socket.sendto(f"login {username} {password}".encode("utf-8"), (server_host, server_port))
        response, _ = client_socket.recvfrom(1024)
        print(response.decode("utf-8"))
        if "Hyrje e suksesshme" in response.decode("utf-8"):
            break

    print("Komanda të disponueshme:")
    print("  list                     - Listo")
    print("  read <filename>          - Lexo")
    print("  write <filename> <text>  - Shkruaj tekst (vetem admin)")
    print("  delete <filename>        - Fshij (vetem admin)")
    print("  send <username> <message> - Dërgo mesazh një përdoruesi")
    print("  exit                     - Dil nga biseda\n")

    while True:
        try:
            message = input("> ")
            if message.lower() == "exit":
                print("Duke dalë nga biseda.")
                break
            client_socket.sendto(message.encode("utf-8"), (server_host, server_port))
            response, _ = client_socket.recvfrom(1024)
            print(response.decode("utf-8"))
        except KeyboardInterrupt:
            print("\nDuke mbyllur klientin.")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()
