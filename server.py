import socket

serversocket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

host = '127.0.0.1'
port = 2205

serversocket.bind((host, port))

while True:
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
    msg = clientsocket.recv(1024)
    print(msg)
    clientsocket.sendall(msg)
    clientsocket.close()
    