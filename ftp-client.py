import socket
from sendcheck import *

HOST = 'localhost'
PORT = 6666
main = True


def command(request):
    try:
        if 'send' in request:
            request, namefile = request.split()
            sendfile(namefile, sock)
        elif 'cat' in request:
            request, namefile = request.split()
            while True:
                msg = sock.recv(1024).decode()
                if 'Ошибка 322' in msg:
                    raise Exception('Ошибка 322!!!')
                elif msg == 'end': 
                    break 
                else: 
                    print(msg, end=' ')
                sock.send('next'.encode())
    except Exception:
        print('Ошибка 322. Файл не найден.')


namefile = ''
accept = False
sock = socket.socket()
sock.connect((HOST, PORT))
while not accept:
    ans = sock.recv(1024).decode()
    print(ans)
    if 'Здесь' in ans:
        accept = True
    else:
        sock.send(input('>').encode())
    

while main:
    request = input('>')
    if request == 'exit':
        main = False
    sock = socket.socket()
    sock.connect((HOST, PORT))
    if 'send' in request:
        try:
            print(request[5:])
            with open(request[5:]) as f:
                pass  
        except FileNotFoundError:
            print('Файл не найден.')
            continue
    sock.send(request.encode())
    command(request)
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()