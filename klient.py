import tkinter as tk
import socket
import threading

def send_msg():
    msg = entry1.get()
    if msg:
        s.send(msg.encode())


def msg_lisener():
    while True:
        msg = s.recv(1024)
        msg = msg.decode('ascii')
        print(msg)
        text1.insert(tk.END, '\n'+msg)

# server
s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

host = '127.0.0.1'
port = 2205
s.connect((host, port))

# Window
root = tk.Tk()
root.title('Chatos')

text1 = tk.Text(
    width = 40,
    height = 40
)
text1.pack()

entry1 = tk.Entry(
    width=30
)
entry1.pack()

threading.Thread(target = msg_lisener).start()

button1 = tk.Button(
    text='odeslat',
    width=20,
    command=lambda: send_msg()
)
button1.pack()

root.mainloop()
s.close()