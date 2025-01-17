"""
It should work independently

    Sending data
    receive input from client and calculate then send 
    
    client -> key_press
    server -> player position, coin position, score, direction <-- graphic
    
    initial
    {
        state: Waiting,
        coin_position: [
            {
                id: 1,
                position: (x, y)
                is_collected: False
            },
            {
                id: 2,
                position: (x, y)
                is_collected: False
            }
        ],

        players,
    }
    
    start_game
    {
        state: Playing 
    }

    players
    {
        id: 1,
        player: {
            center: (x, y),
            direction: (x, y),
            currenct_score: 0
        },
    }
    
    # when coin have collected. Destroy the coin from list and clients screen
    coin_update
    {
        id: 1
        is_colleted: True
    }
"""

import socket
import json
import threading

HOST = "0.0.0.0"
PORT = 5505
MAX_CLIENT_NUMBER = 2

clients = {}


class Client:
    def __init__(self, client_socket: socket.socket, id: str) -> None:
        self.client_socket = client_socket
        self.id = id
        self.data = {}

    def update_data(self, data: dict) -> None:
        """ TODO: check that what data packet should look like """
        self.data = data

    def update_user(self) -> None:
        json_data = (json.dumps(self.data) + '\n').encode()
        self.client_socket.send(json_data)


def broadcast() -> None:
    """ Update to every player """
    for client in clients:
        client.update_user()


def handle_client(client: Client) -> None:
    """ Handle data from each client """
    try:
        while True:
            buffer = b""

            # receiving message
            while True:
                data = client.client_socket.recv(32)

                # receive data as bytes
                if data:
                    buffer += data

                    if buffer.endswith(b'\n'):
                        break
                else:
                    # disconnected
                    print(f"{client.id} has disconnected")
                    raise ConnectionError

            # When we have recieved some data
            if buffer:
                try:
                    # Update data of Client
                    print(f"Upddating data of {client.id}")
                    json_data = json.loads(buffer.strip())
                    client.update_data(json_data)
                    client.client_socket.send("Data recieved".encode())

                    # After update, send an update to every players
                    broadcast()

                    # DEBUG
                    print(f"Player {client.id}'s data")
                    print(json_data)

                except json.JSONDecodeError as e:
                    print(f"Error to decode JSON data: {e}")

    except ConnectionError:
        # Show on the server and send it to everyone
        print(f"{client.id} left the game!")

    finally:
        # clear and remove everything
        if client_socket in clients:
            clients.pop(client.id)
        client_socket.close()


if __name__ == "__main__":
    # intial server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
    except OSError as msg:
        server = None
        print(f"Error creating socket: {msg}")
        exit(1)

    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Socket bound and server is listening on {HOST}:{PORT}")
    except OSError as msg:
        print(f"Error binding/listening!: {msg}")
        server.close()
        exit(1)

    # main loop
    while True:
        client_socket, client_address = server.accept()

        # Check whether players are full now
        if len(clients) >= MAX_CLIENT_NUMBER:
            client_socket.send("Server Room is full now".encode())
            client_socket.shutdown(socket.SHUT_RDWR)
            continue

        # add player to list
        id = len(clients) + 1
        print(f"players {id} joinned")
        clients[id] = Client(client_socket, id)

        # Create new Thread for each player
        client_thread = threading.Thread(
            target=handle_client, args=(clients[id], ))
        client_thread.start()
