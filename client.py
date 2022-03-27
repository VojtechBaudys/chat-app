from base64 import encode
import tkinter as tk
import socket
import threading

def send_msg(event):
    msg = entry_box.get()
    if len(msg) <= 1000:
        s.send(msg.encode('utf8'))
        entry_box.delete(0, tk.END)

def msg_lisener():
    while True:
        msg = s.recv(1000)
        msg = msg.decode('utf8')
        print(msg)
        text_box.config(state='normal')
        text_box.insert(tk.END, msg+'\n')
        text_box.config(state='disabled')

# ---- Connect ----
s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

host = '127.0.0.1'
port = 2205
s.connect((host, port))

# ---- Tkinter ----
root = tk.Tk()
root.title('Tinder')
root.bind("<Return>", lambda event: send_msg(event))

name_entry = tk.Entry(
    width=30
)
name_entry.pack()

password_entry = tk.Entry(
    width=30
)
password_entry.pack()

text_box = tk.Text(
    width = 40,
    height = 40
)
text_box.pack()
text_box.config(state='disabled')

entry_box = tk.Entry(
    width=30
)
entry_box.pack()

button1 = tk.Button(
    text='odeslat',
    width=20,
    bg='pink',
    command=lambda event='': send_msg(event)
)
button1.pack()

threading.Thread(target = msg_lisener).start()

root.mainloop()
s.close()