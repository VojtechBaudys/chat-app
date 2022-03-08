import tkinter as tk
import socket

def send_msg():
    s.send(b'Honza')

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
    height = 50
)
text1.pack()

entry1 = tk.Entry(
    width=30
)
entry1.pack()
 
button1 = tk.Button(
    text='odeslat',
    width=20,
    # command=lambda: s.send(b'Honza')
    command=send_msg
)
button1.pack()

# msg = s.recv(1024)
# msg = msg.decode('ascii')
# print(msg)
# text1.insert(tk.END, '\n'+msg)

root.mainloop()
s.close()