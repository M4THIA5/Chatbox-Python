import socket
import threading
import time
MSGLEN = 256

class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def deconnect(self):
        self.sock.close()

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            try:
                sent = self.sock.send(msg[totalsent:].encode('utf-8'))
                if sent == 0:
                    break
                totalsent += sent
            except Exception as e:
                print(f"Error in mysend: {e}")
                break  # Sort de la boucle si une exception est levée

    
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)


client = MySocket()
# network_ip = input("enter network IP : ")
# listening_port = int(input("Enter listening port : "))
# client.connect(network_ip, listening_port)
client.connect('127.0.0.1', 5000)
while True:
    try:
        message = input("Entrer le message : ")
        if message == "!EXIT":
            break
        else:
            client.mysend(message)
    except Exception as e:
        print(f"Error: {e}")
        break

client.deconnect()