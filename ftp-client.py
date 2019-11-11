import socket

HOST = 'localhost'

PORT = 8888

while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))

	if request=='exit':
            sock.close()
    
    else:
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
sock.close()