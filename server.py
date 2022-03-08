import socket

serversocket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

host = socket.gethostname()
port = 2205

serversocket.bind((host, port))

while True:
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
    clientsocket.sendall(b'Hello world!')
    clientsocket.close()
    