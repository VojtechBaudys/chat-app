from fileinput import close
import json
import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

def close_app(msg): # close app
    try:
        s.send(msg.encode('utf8')) # send disconnect msg to server
    except:
        pass
    root.destroy() # destroy tk window

def leave_login(obj, msg): # login entry mouse leave
	if obj.get() == '':
		obj.delete(0, 'end')
		obj.insert(0, msg)

def enter_login(obj, msg): #login entry mouse enter
    if obj.get() == msg:
        obj.delete(0, 'end')

def send_msg(event): # send msg to server
	msg = entry_box.get() # get msg from entry
	if msg == '/help': # help command
		entry_box.delete(0, tk.END)
        # write commands to text area
		text_box.config(state='normal')
		text_box.insert(tk.END, '\n' + 'COMMANDS' + '\n' + '/online [show online users]' + '\n' + '/offline [show offline users]' + '\n' + '/leave [shut down app]' + '\n')
		text_box.config(state='disabled')
	elif msg == '/online' or msg == '/offline': # offline command
		s.send(msg.encode('utf8')) # send msg
		entry_box.delete(0, tk.END) # clear entry box
	elif msg == '/leave': # leave command
		close_app(msg)
	elif msg != '': # if is not empty
		if len(msg) <= 1000 and msg[0] != '/': # max len msg
			s.send(msg.encode('utf8')) # send normal msg to server
			entry_box.delete(0, tk.END) # clear entry box

def msg_lisener(): # listen server msg when logged
    while True:
        try:
            msg = s.recv(1000) # get msg
        except:
            break
        msg = msg.decode('utf8') # decode msg
        # write msg to text area
        text_box.config(state='normal')
        text_box.insert(tk.END, msg + '\n')
        text_box.config(state='disabled')

def listen_login(): # listen login status
    while True:
        try:
            msg = s.recv(1000) # get loggin status
        except:
            break
        msg = msg.decode('utf8') # decode msg
        if msg == '/success': # login success
            # destroy login form
            login_email.destroy()
            login_password.destroy()
            login_button.destroy()
            login_label.destroy()

            global text_box
            global entry_box
            global button1

            # setup chat
            text_box = scrolledtext.ScrolledText(
                width = 40,
                height = 40,
                wrap="word"
            )
            text_box.pack()
            text_box.insert(tk.END, 'Welcome to the Badoo...' + '\n' + 'HELP COMMAND: /help' + '\n')
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

            threading.Thread(target = msg_lisener).start() # start listening msg
            root.bind('<Return>', lambda event: send_msg(event))

            break

def send_login(): # send login json (email, passowrd)
	email = login_email.get() # get email from entry
	password = login_password.get() # get password from entry
	if email != '' and email != 'Email' and password != '' and password != 'Password': # if is not null
        # create json 
		data = {
			'email': email,
			'password': password
		}
		data = json.dumps(data)
		if len(data) <= 1000:
			s.send(data.encode('utf8')) # send json

# connect to server
s = socket.socket(
	socket.AF_INET,
	socket.SOCK_STREAM
)

host = '127.0.0.1'
port = 2205
s.connect((host, port))

# login form setup
root = tk.Tk()
root.title('Badoo')
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='badoo.png'))

login_label = tk.Label(
	text='LOGIN'
)
login_label.pack()

login_email = tk.Entry(
	width=30
)
login_email.pack()
login_email.insert(0, 'Email')
login_email.bind('<Button-1>', lambda event='': enter_login(login_email, 'Email'))
login_email.bind('<FocusOut>', lambda event='': leave_login(login_email, 'Email'))

login_password = tk.Entry(
	width=30
)
login_password.pack()
login_password.insert(0, 'Password')
login_password.bind('<Button-1>', lambda event='': enter_login(login_password, 'Password'))
login_password.bind('<FocusOut>', lambda event='': leave_login(login_password, 'Password'))

login_button = tk.Button(
	text='login',
	command=lambda: send_login()
)
login_button.pack()

root.bind('<Return>', lambda event: send_login())
root.protocol("WM_DELETE_WINDOW", lambda event='': close_app('/leave'))

threading.Thread(target=listen_login).start()

root.mainloop()
s.close()
