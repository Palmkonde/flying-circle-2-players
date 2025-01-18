import socket
import threading
import json
import pygame
from Arm.graphic import Graphic

# DEBUG
from pprint import pprint

HOST = '127.0.0.1'
PORT = 5505

connecting_status = True
is_first_join = True
game = None 

pygame.init()

class Client:
    def __init__(self, id: int) -> None:
        self.id = id
        self.state = 0
        self.coin_postion = []
        
        # players data
        self.players = {} 

def send_message(server_socket: socket.socket) -> None:
    """ send a message to server """
    global connecting_status
    try:
        while connecting_status:
            keys = pygame.key.get_pressed()
            key_data = {}

            # Check keys and send appropriate data
            if keys[pygame.K_w]:
                key_data["key"] = "w"
            elif keys[pygame.K_a]:
                key_data["key"] = "a"
            elif keys[pygame.K_d]:
                key_data["key"] = "d"

            if key_data:  # If there's any key pressed
                data = {
                    'id': game.id,
                    "key_pressed": key_data['key']
                }
                server_socket.sendall((json.dumps(data) + "\n").encode())

            pygame.time.delay(50)  # Small delay to reduce network load

    except Exception as e:
        print(f"Error in send_key_presses: {e}")
        connecting_status = False
        

def receive_data(sock: socket.socket) -> None:
    global game, connecting_status, is_first_join
    try:
        # receiving messages
        while connecting_status:
            message_received = b""
            while True:
                buffer = sock.recv(32)
                if buffer:
                    print('received data chunk from server: ',
                            repr(buffer))  # DEBUG
                    message_received += buffer
                    if message_received.endswith(b"\n"):
                        break
                else:
                    print("Connection lost!")
                    connecting_status = False
                    break

            json_data = json.loads(message_received.decode())

            # print message that has received
            pprint(json_data)  # DEBUG

            # TODO: put these data into graphic
            # first join create an client object
            if is_first_join:
                game = Client(json_data.get("id"))
                is_first_join = False
                continue

            # Update screen data
            try:
                game.players = json_data.get("players")
                game.state = json_data.get("state")
                game.coin_position = json_data.get("coin_position")
            
            except Exception as e:
                print(f"Error try to update data: {e}")

    except (ConnectionAbortedError, OSError):
        print("Socket Closed")

    finally:
        connecting_status = False
        send_thread.join()
        print("Existing Client...")

def run_game() -> None:
    global game
    
    graphic = Graphic()
    graphic.fetch_data()
    graphic.run_main()

if __name__ == "__main__":
    """ Open socket to connect the server """ 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connected to server")

        # Thread for send a message
        send_thread = threading.Thread(target=send_message, args=(sock,))
        receive_thread = threading.Thread(target=receive_data, args=(sock,))
        
        # start Thread
        send_thread.start()
        receive_thread.start()

        # main_game
        run_game()

    print("Client Closed")
