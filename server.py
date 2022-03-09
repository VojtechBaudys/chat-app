import socket
import threading

def lis():
    while True:
        msg = clientsocket.recv(1024)
        if msg:
            print(msg)
            print(addr)
            clientsocket.sendall(msg)
        # clientsocket.close()

serversocket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

host = '192.168.88.23'
port = 2205

serversocket.bind((host, port))

while True:
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
    threading.Thread(target=lis())

    