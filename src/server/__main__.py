import socket
import threading
import queue
import util


IP = "0.0.0.0"
PORT = 2023


def _client_listen(client: socket.socket, messages: queue.Queue) -> None:
    while True:
        msg = client.listen(1024)
        messages.put(msg)


def _client_send(client: socket.socket, messages: queue.Queue) -> None:
    while True:
        msg = messages.get()
        client.send(msg)


def handle_client(client: socket.socket, messages: queue.Queue) -> None:
    listen = threading.Thread(target=_client_listen, args=(client, messages))
    listen.start()

    send = threading.Thread(target=_client_send, args=(client, messages))
    send.start()


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((IP, PORT))
        server.listen()

        while True:
            client, address = server.accept()


if __name__ == "__main__":
    main()
