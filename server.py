import json
import socket
import threading

def listen():
    while True:
        serversocket.listen()
        clientsocket = serversocket.accept()[0]
        print(clientsocket)
        clients.append({'id': len(clients) ,'logged': False, 'socket': clientsocket, 'username': ''})
        threading.Thread(target=user_handler, args=(clients[-1],)).start()
        
def user_handler(client):
    print(client)
    while client:
        if client['logged']:
            msg = client['socket'].recv(1000).decode('utf8')
            if msg:
                print(msg)
                if msg == '/users':
                    msg = '\n\nUSERS\n'
                    for one_client in clients:
                        msg += one_client['username'] + '\n'
                    print(client)
                    client_msg(client['socket'], msg)
                elif msg == '/leave':
                    clients.pop(client['id'])
                    client = False
                    print(clients)
                    print(client)
                else:
                    send_msg(client['username'], msg)
        else:
            res = client['socket'].recv(1000).decode('utf8')
            print(res)
            res = json.loads(res)
            with open('user_data.json', 'r') as us:
                user_data = json.load(us)
            try:
                if user_data[res['email']]:
                    if user_data[res['email']]['password'] == res['password']:
                        clients[client['id']]['logged'] = True
                        clients[client['id']]['username'] = user_data[res['email']]['name']
                        client_msg(client['socket'], '/success')
                        print(client)
                    else:
                        client_msg(client['socket'], '/error')
                else: 
                    client_msg(client['socket'], '/error')
            except:
                client_msg(client['socket'], '/error')

def client_msg(client, msg):
    msg = msg.encode('utf8')
    client.send(msg)

def send_msg(username, msg):
    msg = (username + ': ' + msg).encode('utf8')
    for client in clients:
        client['socket'].send(msg)

clients = []
serversocket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
host = '127.0.0.1'
port = 2205

try:
    serversocket.bind((host, port))

    lis = threading.Thread(target=listen)
    lis.start()
    lis.join()

    serversocket.close()
except:
    print('error')
