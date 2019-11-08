import socket, os

HOST = 'localhost'
PORT = 6666

while True:
	request = input('>')
	
	if request == 'exit':
		print('Клиент закрыт')
		break
	
	elif request == 'clear':
		try:
			os.system('clear')
			os.system('cls')
		except:
			pass
	
	else:
		sock = socket.socket()
		sock.connect((HOST, PORT))
		
		sock.send(request.encode())
		
		response = sock.recv(1024).decode()
		print(response)
		
		sock.close()