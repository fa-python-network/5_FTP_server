import socket
import os
from sendcheck import *
from time import sleep


'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')
os.chdir('docs')
def process(req):
    try:
        try:
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
                try:
                    req, namedir = req.split(' ')
                    os.rmdir(namedir)
                    return f'Папка {namedir} удалена.'
                except OSError:
                    return 'Папка не пуста!'
            elif 'chdir' in req:
                try:
                    req, namedir = req.split(' ')
                    os.chdir(namedir)
                    dirname = os.path.join(os.getcwd())
                except FileNotFoundError:
                    pass
                return f'Текущая директория {os.getcwd()}'
            elif 'rename' in req:
                req, namedir, newname = req.split(' ')
                os.rename(namedir, newname)
                return f'Папка {namedir}, успешно переименована в {newname}.'
            elif 'send' in req:
                req, namefile = req.split(' ')
                checkfile(namefile,conn)
                return 'Файл принят.'
            elif 'cat' in req:
                req, namefile = req.split(' ')
                sendfile(namefile, conn)
                return f'Содержимое файла {namefile}'
            elif 'remove' in req:
                req, namefile = req.split(' ')
                os.remove(namefile)
                return 'Файл удален.'
            
            return 'bad request'
        
        except ValueError:
            return 'Некоректно введенная команда.'
    
    except FileNotFoundError:
        conn.send('Ошибка 322. Не найден указанный путь.'.encode())
        sleep(0.001)
        return 'Попробуйте еще раз.'
        

PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    try:
        conn, addr = sock.accept()
        
        request = conn.recv(1024).decode()
        
        
        response = process(request)
        conn.send(response.encode())
    except (ConnectionError, KeyboardInterrupt):
        continue

conn.close()
