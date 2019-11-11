#
#
import socket

port = 10000
lh = 'localhost'

while True:
    req = input('>')
    
    sock = socket.socket()
    sock.connect((lh, port))
    
    sock.send(req.encode())
    
    res = sock.recv(1024).decode()
    print(res)
    
    if req == 'cquit':
        sock.close()
        break
