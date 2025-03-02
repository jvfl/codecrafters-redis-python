import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, _ = server_socket.accept()

    while True:
        # Read the first command from the client.
        client_message = connection.recv(4096)
        print(f"Received message: {client_message}")
        pings = [ping for ping in client_message.splitlines() if ping == b"PING"]

        for _ in pings:
            connection.sendall(b"+PONG\r\n")


if __name__ == "__main__":
    main()
