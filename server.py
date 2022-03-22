import socket
import threading

def listen():
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()    
        clientsocket.send(b'connected')
        print(clientsocket)
        clients.append(clientsocket)
        threading.Thread(target=user_handler, args=(clientsocket,)).start()

def user_handler(client):
    print('handler/////////////')
    print(client)
    while True:
        msg = client.recv(1024)
        if msg:
            print(msg)
            send_msg()

def send_msg():
    

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