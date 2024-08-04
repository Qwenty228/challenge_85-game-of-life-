import socket
import os
import threading
from dotenv import load_dotenv
import pickle


load_dotenv()

class Network:
    """A class to handle the network communication between the client and the server."""
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.disconnected = False
      

    def connect(self):
        self.client.connect((os.environ.get("HOST"), int(os.environ.get("PORT"))))
        receive_thread = threading.Thread(target=self.__communication)
        receive_thread.start()

    def __communication(self):
        try:
            while True:
                message = self.client.recv(1024).decode()
                if not message:
                    break
                print(f"Received: {message}")
        except ConnectionResetError:
            pass
        finally:
            self.client.close()
            self.disconnected = True
