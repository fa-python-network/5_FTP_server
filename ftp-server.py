import socket
import os
from sendcheck import *


'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')
os.chdir('docs')
def process(req):
    global dirname
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        if os.listdir(dirname) != []:
            return '; '.join(os.listdir(dirname))
        else: return 'Папка пуста.'

    elif 'mkdir' in req:
        req, namedir = req.split(' ')
        os.mkdir(namedir)
        return f'Папка {namedir} создана.'
    elif req == 'exit':
        return 'Прощай!'
    elif 'rmdir' in req:
        req, namedir = req.split(' ')
        os.rmdir(namedir)
        return f'Папка {namedir} удалена.'
    elif 'chdir' in req:
        req, namedir = req.split(' ')
        dirname = os.path.join(os.getcwd(), namedir)
        os.chdir(namedir)
        return f'Текущая директория {os.getcwd()}'
    elif 'rename' in req:
        req, namedir, newname = req.split(' ')
        os.rename(namedir, newname)
        return f'Папка {namedir}, успешно переименована в {newname}.'
    return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    
    
    response = process(request)
    conn.send(response.encode())

conn.close()
