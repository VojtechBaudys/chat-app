import socket
import threading

def listen():
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        connected = 'Connected to Tinder'
        clientsocket.send(connected.encode('utf8'))
        clients.append(clientsocket)
        threading.Thread(target=user_handler, args=(clientsocket,)).start()
        
def user_handler(client):
    print(client)
    while True:
        msg = client.recv(1000)
        if msg:
            print(msg)
            send_msg(msg)

def send_msg(msg):
    for client in clients:
        client.send(msg)

clients = []
serversocket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
host = '127.0.0.1'
port = 2205
serversocket.bind((host, port))

lis = threading.Thread(target=listen)
lis.start()
lis.join()

serversocket.close()