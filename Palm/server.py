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
from math import pi
from Eng.game_engine import GameEngine, PlayerCircle, key_apply


# DEBUG Tool
from pprint import pprint

HOST = "0.0.0.0"
PORT = 5505

PLAYER1_CENTER = (200, 400)
PLAYER2_CENTER = (300, 400)
PLAYER_RADIUS = 50


class Client:
    def __init__(self, client_socket: socket.socket, id: str) -> None:
        self.client_socket = client_socket
        self.id = id

    def update_user(self, data: dict) -> None:
        try:
            json_form = json.dumps(data)
            self.client_socket.sendall((json_form + '\n').encode())

        except Exception as e:
            print(f"error to update user: {e}")


class Server():
    MAX_CLIENT_NUMBER = 2

    def __init__(self) -> None:
        self.clients = {}
        self.user_input = {}
        self.game_state = {}

        player1 = PlayerCircle(id=1, center=PLAYER1_CENTER,
                               radius=PLAYER_RADIUS, direction=0)
        player2 = PlayerCircle(id=2, center=PLAYER2_CENTER,
                               radius=PLAYER_RADIUS, direction=pi)

        self.engine = GameEngine(player1=player1, player2=player2)

    def broadcast(self, data: dict) -> None:
        """ Update to every player """

        for id, client in self.clients.items():
            try:
                client.update_user(data)

            except Exception as e:
                print(f"error broadcasting to {id}: {e}")

                # Handle if client not appear in clients
                if id in self.clients:
                    self.clients.pop(id)
                    client.client_socket.close()

    def handle_client(self, client: Client) -> None:
        """ Handle data from each client """
        try:
            # send player an id
            # print(client.id, type(client.id)) # DEBUG
            id_dict = {"id": client.id}
            client.client_socket.send(
                (json.dumps(id_dict) + '\n').encode('utf-8'))

            while True:
                buffer = b""

                # receiving user input
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
                        print(f"Upddating player {client.id}'s data")  # DEBUG
                        # client.client_socket.send("Data recieved".encode()) # DEBUG

                        json_data = json.loads(buffer.strip())
                        self.user_input = json_data

                        player1_input = None
                        player2_input = None

                        if self.user_input.get('id') == 1:
                            player1_input = self.user_input.get('key_pressed')

                        elif self.user_input.get('id') == 2:
                            player2_input = self.user_input.get('key_pressed')

                        self.game_state = self.engine.run(
                            player1key=key_apply(player1_input),
                            # TODO: waiting for Eng
                            player2key=key_apply(player2_input))

                        # After update, send an update to every players
                        self.broadcast(self.game_state)

                        # DEBUG
                        print(f"Player {client.id}'s data updated")
                        # print(f"Player {client.id}'s data")
                        # print(json_data)

                    except json.JSONDecodeError as e:
                        print(f"Error to decode JSON data: {e}")

        except ConnectionError:
            # Show on the server and send it to everyone
            print(f"{client.id} left the game!")

        finally:
            # clear and remove everything
            if client.id in self.clients:
                self.clients.pop(client.id)
            client.client_socket.close()

    def run_server(self) -> None:
        """ run main server """

        # initial server
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
            if len(self.clients) >= self.MAX_CLIENT_NUMBER:
                client_socket.send("Server Room is full now".encode())
                client_socket.shutdown(socket.SHUT_RDWR)
                continue

            # add player to list
            id = len(self.clients) + 1
            print(f"players {id} joinned")
            self.clients[id] = Client(client_socket, id)

            # Create new Thread for each player
            client_thread = threading.Thread(
                target=self.handle_client, args=(self.clients[id], ))
            client_thread.start()


if __name__ == '__main__':
    server = Server()
    server.run_server()
