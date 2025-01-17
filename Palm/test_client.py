import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5505 

connecting_status = True


DUMMY_DATA = {
    "state": 12,
    "roate_left": "12",
    "roate_right": 50,
}

def send_message(server_socket: socket.socket) -> None:
    """ send a message to server """
    global connecting_status
    while connecting_status:
        message = input(">")  

        if message.lower() == "!exit":
            server_socket.shutdown(socket.SHUT_RDWR) 
            server_socket.close()
            connecting_status = False
            break
            
        if message.lower() == "!send":
            json_data = json.dumps(DUMMY_DATA)
            server_socket.send((json_data + '\n').encode())

if __name__ == "__main__":
    """ Open socket to connect the server """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connected to server")

        # Thread for send a message
        send_thread = threading.Thread(target=send_message, args=(sock,))
        send_thread.start()

        try:
            # receiving messages
            while connecting_status:
                message_received = ""
                while True:
                    data = sock.recv(32)
                    if data:
                        print('received data chunk from server: ', repr(data))
                        message_received += data.decode()
                        if message_received.endswith("\n"):
                            break
                    else:
                        print("Connection lost!")
                        connecting_status = False
                        break
                print(message_received)

        except (ConnectionAbortedError, OSError):
            print("Socket Closed")
        
        finally:
            connecting_status = False
            send_thread.join()
            print("Existing Client...")

    print("Client Closed")
