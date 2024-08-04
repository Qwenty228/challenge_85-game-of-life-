import socket
import threading
import os
from dotenv import load_dotenv

load_dotenv()

# Global flag to indicate server shutdown
shutdown_flag = threading.Event()
server = None

def handle_client(client_socket, addr):
    try:
        while not shutdown_flag.is_set():
            message = client_socket.recv(1024).decode()
            if not message:
                break
            if message == "DISCONNECT":
                print(f"Client {addr} disconnected")
                break
            print(f"Received from {addr}: {message}")
            client_socket.send("Pong".encode())
    except ConnectionResetError:
        pass
    finally:
        client_socket.close()

def start_server():
    global server
    host, port = os.environ.get("HOST"), int(os.environ.get("PORT"))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    server.settimeout(1)
    print(f"Server listening on {host}:{port}")

    try:
        while not shutdown_flag.is_set():
            try:
                client_socket, addr = server.accept()
                print(f"Accepted connection from {addr}")
                client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
                client_handler.start()
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        shutdown_flag.set()
        server.close()


def stop_server():
    global server
    if server is None:
        raise ValueError("Server is not running")

    shutdown_flag.set()
    server.close()

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 12345
    start_server(HOST, PORT)
