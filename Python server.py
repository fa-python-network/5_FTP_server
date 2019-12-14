import socket
import os 
import shutil

port = 1506

sock = socket.socket()
sock.bind(('', port))
sock.listen(0)

conn,addr = sock.accept()

while True:
	msg = conn.recv(1024).decode()
	if msg == 'exit':
		answer = ''
		break
	elif msg == 'cp':
		file_name = conn.recv(1024).decode()
		with open(os.path.join(os.getcwd(), file_name), 'r') as f:
			data = f.read()
		conn.send(data.encode())
	elif msg == 'down':
		file_name = conn.recv(1024).decode()
		file_data = conn.recv(1024).decode()
		data = open(file_name, 'w')
		data.write(file_data)
		data.close()
	elif msg.split()[0] == 'mv':
		os.rename(os.path.join(os.getcwd(), msg.split()[1]), os.path.join(os.getcwd(), msg.split()[2]))
		answer = ' '
	elif msg.split()[0] == 'ls':
		answer = ('; '.join(os.listdir(os.getcwd())))
	elif msg.split()[0] == 'touch':
		file_name = ' '.join(msg.split()[1:])
		
		open(file_name, 'w').close()
		answer = ''
	elif msg.split()[0] == 'cat':
		file_data = open(' '.join(msg.split()[1:]), 'r').read()
		answer = (file_data)
	elif msg.split()[0] == 'mkdir':
		dir_name = ' '.join(msg.split()[1:])
		os.mkdir(os.path.join(os.getcwd(), dir_name))
		answer = ''
	elif msg.split()[0] == 'rm':
		file_name =' '.join(msg.split()[1:])
		os.remove(os.path.join(os.getcwd(),file_name))
	elif msg.split()[0] == 'rmD':
		shutil.rmtree(os.path.join(os.getcwd(), ' '.join(msg.split()[1:])))
	else:
		answer = (msg)
	conn.send(answer.encode())


sock.close()
