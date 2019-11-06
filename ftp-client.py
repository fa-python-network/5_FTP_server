import socket
from logger import Logfile

HOST = 'localhost'
try:
    port=int(input("ваш порт:"))
    if not 0 <= port <= 65535:
        raise ValueError
except ValueError :
    port = 9090

status=True
s=True
while status:
    sock = socket.socket()
    sock.connect((HOST, port))
    l=Logfile()
    l.serverstart()
    while s:
        request = input('>')
        sock.send(request.encode())
        response = sock.recv(1024).decode()
        print(response)
        if request == 'exit':
            status=False
            s=False
    sock.close()