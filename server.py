import socket
import os

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

PORT = 1252
curr_dir = os.path.join(os.getcwd(), 'docs')


def process(req):
    if req == 'exit':
        return 'exit'
    elif req == 'pwd':
        return curr_dir
    elif req == 'ls':
        return '; '.join(os.listdir(curr_dir))
    elif req[:4] == 'cat ':
        filename = req[4:]
        try:
            filename = curr_dir + '/' + filename
            with open(filename) as f:
                return f.read()
        except:
            return "NET TAKOGO FAILA!!!!!!!!!!!!!!"

    else:
        return 'bad request'


sock = socket.socket()
sock.bind(('', PORT))

sock.listen(0)
while True:
    print("Слушаем порт")
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())
    conn.close()
    if request == 'exit':
        print("Client otrubil server nafig")
        break

