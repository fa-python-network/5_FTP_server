import socket

PORT = 6666
HOST = 'localhost'

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    if request == 'quit':
        sock.close()
        break