import socket
import os

host = 'localhost'
port = 1506

sock = socket.socket()

sock.connect((host,port))

while True:
	msg = input()
	if msg == 'exit':
		sock.send(msg.encode())
		break
	elif msg.split()[0] == 'down':
		sock.send('down'.encode())
		sock.send(' '.join(msg.split()[1:]).encode())
		with open(os.path.join(os.getcwd(), ' '.join(msg.split()[1:])), 'r') as f:
			data = f.read()
		sock.send(data.encode())
	elif msg.split()[0] == 'cp':
		sock.send('cp'.encode())
		sock.send(' '.join(msg.split()[1:]).encode())
		file_data = sock.recv(1024).decode()
		data = open(' '.join(msg.split()[1:]), 'w')
		data.write(file_data)
		data.close()
	else:
		sock.send(msg.encode())
		break
	answer = sock.recv(1024).decode()
	print(answer)
	
    
sock.close()
    
