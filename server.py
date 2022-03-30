import json
import socket
import threading
import time
import logging

# logging config
logging.basicConfig(level=logging.DEBUG, filename='server.log', filemode='w', format='[%(asctime)s] [%(levelname)s]: %(message)s')

# functions
def listen(): # listen new clients
    id = 0
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        logging.info(addr[0] + ' connected to server') # log client connected
        clients.append({'id': id ,'logged': False, 'socket': clientsocket, 'addr': addr[0], 'username': ''}) # client vars
        id += 1
        threading.Thread(target=user_handler, args=(clients[-1],)).start() # client thread
        
def user_handler(client): # client handler
    while client:
        if client['logged']: # is logged
            try:
                msg = client['socket'].recv(1000).decode('utf8') # get client msg
            except:
                break
            if msg: # entry msg
                if msg == '/online': # online clients commands
                    msg = '\nONLINE USERS\n'
                    for one_client in clients:
                        msg += one_client['username'] + '\n'
                    client_msg(client['socket'], msg) # send online users
                elif msg == '/offline': # offline clients command
                    msg = '\nOFFLINE USERS\n'
                    with open('user_data.json', 'r') as us:
                        users = json.load(us)
                    for user_db in users:
                        offline = True
                        for user_list in clients:
                            if users[user_db]['name'] == user_list['username'] and user_list['logged']: # if user is logged/connected
                                offline = False
                                break
                        if offline:
                            msg += users[user_db]['name'] + '\n'
                    client_msg(client['socket'], msg) # send offline users
                elif msg == '/leave': # disconnect command
                    remove_client(client['id'], client['addr']) # remove user from connected clients
                else:
                    logging.info(client['username'] + ' send message: "' + msg + '"') # log user msg
                    send_msg(client['username'], msg) # send msg to all logged users
        else: # is not logged
            try:
                res = client['socket'].recv(1000).decode('utf8') # get client email and password / disconnect command
            except:
                break
            if res == '/leave': # disconnect client
                remove_client(client['id'], client['addr']) # remove user from connected clients
                break
            res = json.loads(res) # load user email and password
            with open('user_data.json', 'r') as us: # load user data 
                user_data = json.load(us)
            try:
                if user_data[res['email']]: # if email exist
                    if user_data[res['email']]['password'] == res['password']: # if password is correct
                        clients[client['id']]['logged'] = True # change to logged True
                        clients[client['id']]['username'] = user_data[res['email']]['name'] # set client username
                        client_msg(client['socket'], '/success') # send success msg
                        logging.info(client['username'] + ' logged to Badoo') # log logged client
                    else:
                        client_msg(client['socket'], '/error') # send error msg
                else: 
                    client_msg(client['socket'], '/error') # send error msg
            except:
                client_msg(client['socket'], '/error') # send error msg

def client_msg(client, msg): # send msg to one client
    msg = msg.encode('utf8')
    client.send(msg)

def send_msg(username, msg): # send msg to all clients
    msg = (time.strftime('%m/%d/%Y', time.localtime()) + ' ' + username + ': ' + msg).encode('utf8')
    for client in clients:
        client['socket'].send(msg)

def remove_client(id, addr): # disconnect client
    clients.pop(id)
    logging.info(addr + ' disconnected from server') # log disconnected client
    client = False
    
clients = []

# Server
serversocket = socket.socket( 
    socket.AF_INET,
    socket.SOCK_STREAM
)
host = '127.0.0.1'
port = 2205

try:
    serversocket.bind((host, port))

    lis = threading.Thread(target=listen) # main listen thread
    lis.start()
except Exception as e: # main start error
    logging.error(str(e) + ' (Line: ' + str(e.__traceback__.tb_lineno) + ')') # log server start error
else:
    logging.info('server started') # log server started

lis.join()

serversocket.close() # server socket close
