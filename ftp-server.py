import socket
import os
from sendcheck import *
from time import sleep
import json

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''
os.chdir('docs')
maindir = os.path.join(os.getcwd())
def process(req, root):
    try:
        try:
            global dirname
            global accept
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
                accept = False
                os.chdir(maindir)
                return 'Прощай!'
            elif 'rmdir' in req:
                try:
                    req, namedir = req.split(' ')
                    os.rmdir(namedir)
                    return f'Папка {namedir} удалена.'
                except OSError:
                    return 'Папка не пуста!'
            elif 'cd' in req:
                try:
                    req, namedir = req.split(' ')
                    os.chdir(namedir)
                    if usname not in os.getcwd()[42:] and not root:
                        os.chdir(dirname)
                        raise Exception
                    dirname = os.path.join(os.getcwd())
                except (FileNotFoundError, Exception):
                    return f'Нет доступа или неверное название папки! Текущая директория {os.getcwd()}'
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
            elif 'newad' in req and root:
                req, newname, newpass, acce = req.split(' ')
                if acce.lower() == 'true':
                    acce = True
                else:
                    acce = False
                names[newname] = [newpass, acce]
                os.chdir(maindir)
                os.mkdir(newname)
                with open('names.json', 'w') as file:
                    json.dump(names, file)
                os.chdir(dirname)
                return f'Новый пользователь {newname}, создан.'
            
            return 'bad request'
        
        except ValueError:
            return 'Некоректно введенная команда.'
    
    except FileNotFoundError:
        conn.send('Ошибка 322. Не найден указанный путь.'.encode())
        sleep(0.001)
        return 'Попробуйте еще раз.'


accept = False
PORT = 6666


sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
with open('names.json', 'r') as file:
    names = json.load(file)
print("Прослушиваем порт", PORT)
while True:
    conn, addr = sock.accept()
    conn.send('Добро пожаловать. Введите имя пользователя:'.encode())
    while not accept:
        usname = conn.recv(1024).decode()
        
        if usname in names:
            conn.send(f'Дарова {usname}! Введите пароль:'.encode())
            passw = conn.recv(1024).decode()
            if names[usname][0] == passw:
                accept = True
                root = names[usname][1]
                os.chdir(usname)
                dirname = os.path.join(os.getcwd())
            else:
                conn.send('Не верный пароль! Снова введите имя пользователя:'.encode())
        
        else:
            conn.send(f'Дарова Неизвестный! Введите новый пароль:'.encode())
            passw = conn.recv(1024).decode()
            with open('names.json', 'w') as file:
                names[usname] = [passw, False]
                json.dump(names, file)
            root = False
            os.mkdir(usname)
            os.chdir(usname)
            dirname = os.path.join(os.getcwd())
            accept = True
        if accept:
            conn.send('Здесь сегодня тесновато.. Но для тебя всегда место найдется!'.encode())


    while accept:
        try:
            conn, addr = sock.accept()
            
            request = conn.recv(1024).decode()
            
            response = process(request, root)
            conn.send(response.encode())
        except (ConnectionError, KeyboardInterrupt):
            continue

conn.close()
