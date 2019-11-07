
import socket
import os
from logger import Logfile
from func import process



try:
    port=int(input("ваш порт:"))
    if not 0 <= port <= 65535:
        raise ValueError
except ValueError :
    port = 9090

'''
l=Logfile()
l.serverstart()
'''

sock = socket.socket()
sock.bind(('', port))
sock.listen()
print("Прослушиваем порт", port)

while True:
    conn, addr = sock.accept()
    
    while True:
        request = conn.recv(1024).decode()
        if request == "":
            break
    
        response = process(request,conn)
        conn.send(response.encode())
    conn.close()



