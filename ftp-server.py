import socket
import os
import re
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        print(req.split(' '))
        print(re.findall(r'^\w*', req.split(' ')))
        return '; '.join(os.listdir(dirname))
#    elif 'mkdir' == str(mkdir.findall(str(req))):
#    elif 'mkdir' == str(re.findall(r'\w+^', req.split(' '))):
#        return 'lalala' 
#    elif req == 'cat ' + 
    return 'bad request'


PORT = 9090

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()
