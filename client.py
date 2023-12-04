import socket
import threading
import keyboard
import time

MSGLEN = 256
run = True

class MySocket:
    def __init__(self, sock=None):
        # Constructor to initialize the socket object.
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        # Connect to the specified host and port.
        self.sock.connect((host, port))
        
        print("To write message press : CTRL")
        print("To leave the discussion press : ECHAP")

    def deconnect(self):
        # Close the socket connection.
        global run
        run = False
        self.sock.close()

    def mysend(self, msg):
        # Send a message over the socket.
        totalsent = 0
        while totalsent < MSGLEN:
            try:
                sent = self.sock.send(msg[totalsent:].encode('utf-8'))
                if sent == 0:
                    break
                totalsent += sent
            except Exception as e:
                # Handle any exceptions that may occur during sending.
                print(f"Error in mysend: {e}")
                break

    def write_message(self):
        try:
            # Prompt user for a message and send it when the space key is pressed.
            message = input("Enter the message: ")
            if len(message)>0 and message != ' ':
                self.mysend(message)
        except Exception as e:
            # Handle any exceptions that may occur during message input or sending.
            print(f"Error: {e}")

    def myreceive(self):
        # Receive a message from the socket.
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

while run:
    if keyboard.is_pressed('ctrl'):
        client.write_message()
    elif keyboard.is_pressed('esc'):
        client.deconnect()
    else:
        time.sleep(0.5)