import socket
from sendcheck import *

HOST = 'localhost'
PORT = 6666
main = True

while main:
    request = input('>')
    if request == 'exit':
        main = False
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    if 'send' in request:
        request, namefile = request.split(' ')
        sendfile(namefile, sock)
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()