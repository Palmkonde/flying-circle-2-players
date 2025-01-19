import socket
import threading
import json
import pygame
from Arm.graphic2 import Graphics

# DEBUG
from pprint import pprint

HOST = '127.0.0.1'
PORT = 5505

# states 
connecting_status = True
is_first_join = True
game = None 
share_data = {}
ready_get_id = threading.Event()

pygame.init()

class Client:
    def __init__(self, id: int) -> None:
        self.id = id

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
            elif keys[pygame.K_SPACE]:
                key_data["key"] = "space"

            if key_data:  # If there's any key pressed
                data = {
                    'id': game.id,
                    "key_pressed": key_data['key']
                }
                server_socket.sendall((json.dumps(data) + "\n").encode())

            pygame.time.delay(100)  # Small delay to reduce network load

    except Exception as e:
        print(f"Error in send_key_presses: {e}")
        connecting_status = False
        

def receive_data(sock: socket.socket) -> None:
    global game, connecting_status, is_first_join, share_data
    
    buffer = bytearray()
    try:
        # receiving messages
        while connecting_status:
            message_received = b""
            while True:
                buffer = sock.recv(32)
                if buffer:
                    # print('received data chunk from server: ', repr(buffer))  # DEBUG 
                    message_received += buffer
                    if message_received.endswith(b"\n"):
                        break
                else:
                    print("Connection lost!")
                    connecting_status = False
                    break
            
            # Process each JSON object separated by '\n'
            for json_message in message_received.split(b"\n"):
                if json_message.strip():  # Skip empty lines
                    try:
                        json_data = json.loads(json_message)
                        # pprint(json_data)  # DEBUG

                        # First join: create a Client object
                        if is_first_join:
                            game = Client(json_data.get("id"))
                            is_first_join = False
                            continue

                        # Update screen data
                        try:
                            share_data.update(json_data)

                            # print(f"this is share data in client: {share_data}") # DEBUG
                            if ready_get_id.is_set():
                                continue
                            ready_get_id.set()
                        except Exception as e:
                            print(f"Error updating data: {e}")

                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON: {e}, message: {json_message}")


    except (ConnectionAbortedError, OSError):
        print("Socket Closed")

    finally:
        connecting_status = False
        send_thread.join()
        print("Existing Client...")

def run_game() -> None:
    global share_data, game

    # Wait for initial data
    while not ready_get_id.is_set():
        print("Waiting for data...")

    # Graphics instance
    graphic = Graphics(screen=(1200, 750), share_data=share_data)

    # Run the graphics loop
    graphic.run_graphics()


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
