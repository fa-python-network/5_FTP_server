import socket
from sendcheck import *

HOST = 'localhost'
PORT = 6666
main = True


def command(request, namefile):
    try:
        if 'send' in request:
            sendfile(namefile, sock)
        elif 'cat' in request:
            while True:
                msg = sock.recv(1024).decode()
                if 'Ошибка 322' in msg:
                    raise Exception('Ошибка 322!!!')
                elif msg == 'end': 
                    break 
                else: 
                    print(msg)
                sock.send('next'.encode())
    except Exception:
        print('Ошибка 322. Файл не найден.')


namefile = ''

while main:
    request = input('>')
    if request == 'exit':
        main = False
    sock = socket.socket()
    sock.connect((HOST, PORT))
    if 'send' in request:
        request, namefile = request.split(' ')
        try:
            with open(namefile) as f:
                pass
        except FileNotFoundError:
            print('Файл не найден.')
            continue
    sock.send(request.encode())
    command(request, namefile)
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()