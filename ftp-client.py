import socket

HOST = 'localhost'

while True:
	PORT = input('Your port: ')
	if 1024<int(PORT)<=65525:
		print('good')
		break
	else:
		print('try another port')

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, int(PORT)))
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()