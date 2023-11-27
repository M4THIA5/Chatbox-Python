import socket
import threading
import time

class ClientThread(threading.Thread):
    def __init__(self, client_socket, address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address

    def run(self):
        print(f"Accepted connection from {self.address}")

        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break  # Si les données sont vides, la connexion est fermée
                print(f"Received data from {self.address}: {data.decode('utf-8')}")
                self.client_socket.sendall(data)
        except ConnectionResetError:
            print(f"Connection reset by peer ({self.address})")
            self.client_socket.close()
        except Exception as e:
            print(f"Error in run: {e}")

        



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5000))
server_socket.listen()

print("Server listening on port 5000")

while True:
    (client_socket, address) = server_socket.accept()

    client_thread = ClientThread(client_socket, address)
    client_thread.start()
    time.sleep(0.5)