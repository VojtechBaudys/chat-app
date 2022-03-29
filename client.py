import json
import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

def leave_login(obj, msg):
	if obj.get() == '':
		obj.delete(0, 'end')
		obj.insert(0, msg)

def send_msg(event):
	msg = entry_box.get()
	if msg == '/help':
		entry_box.delete(0, tk.END)
		text_box.config(state='normal')
		text_box.insert(tk.END, '\n' + 'COMMANDS' + '\n' + '/users' + '\n' + '/leave')
		text_box.config(state='disabled')
	elif msg == '/users':
		s.send(msg.encode('utf8'))
		entry_box.delete(0, tk.END)
	elif msg == '/leave':
		s.send(msg.encode('utf8'))
		root.destroy()
	elif msg != '':
		if len(msg) <= 1000 and msg[0] != '/':
			s.send(msg.encode('utf8'))
			entry_box.delete(0, tk.END)

def msg_lisener():
	while True:
		msg = s.recv(1000)
		msg = msg.decode('utf8')
		print(msg)
		text_box.config(state='normal')
		text_box.insert(tk.END, msg + '\n')
		text_box.config(state='disabled')

def listen_login():
	while True:
		msg = s.recv(1000)
		msg = msg.decode('utf8')
		print(msg)
		if msg == '/success':
			login_email.destroy()
			login_password.destroy()
			login_button.destroy()
			login_label.destroy()
			
			global text_box
			global entry_box
			global button1

			text_box = scrolledtext.ScrolledText(
				width = 40,
				height = 40,
				wrap="word"
			)
			text_box.pack()
			text_box.insert(tk.END, 'Welcome to the Tinder...' + '\n')
			text_box.config(
				state='disabled',
			)

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
			root.bind('<Return>', lambda event: send_msg(event))

			break

def send_login():
	email = login_email.get()
	password = login_password.get()
	if email != '' and email != 'Email' and password != '' and password != 'Password':
		data = {
			'email': email,
			'password': password
		}
		data = json.dumps(data)
		if len(data) <= 1000:
			s.send(data.encode('utf8'))
	print('login')

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

login_label = tk.Label(
	text='LOGIN'
)
login_label.pack()

login_email = tk.Entry(
	width=30
)
login_email.pack()
login_email.insert(0, 'Email')
login_email.bind('<Button-1>', lambda event='': login_email.delete(0, 'end'))
login_email.bind('<FocusOut>', lambda event='': leave_login(login_email, 'Email'))

login_password = tk.Entry(
	width=30
)
login_password.pack()
login_password.insert(0, 'Password')
login_password.bind('<Button-1>', lambda event='': login_password.delete(0, 'end'))
login_password.bind('<FocusOut>', lambda event='': leave_login(login_password, 'Password'))

login_button = tk.Button(
	text='login',
	command=lambda: send_login()
)
login_button.pack()

root.bind('<Return>', lambda event: send_login())

threading.Thread(target=listen_login).start()

root.mainloop()
s.close()
