import socket
import os
import requests
import json
import shutil


'''
pwd - показывает название рабочей директории
ls - содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <Название папки> - создает новую папку
rmdir <Название папки> - удаляет папку
create <Название файла> <Содержимое файла> - создает файл, если передано сожержимое, то записывает содержимое в этот файл
remove <Название файла> - удаляет файл
rename <Название файла> - переименовывает файл
copy <Название файла> <Название нового файла> - копирует содержимое первого файла во второй

Если вдруг вам понадобилось УЗНАТЬ ПОГОДУ на 3 дня вперед в FTP СЕРВЕРЕ, то наберите команду: 
wheather <city> - узнать погоду в текущем городе
'''


def process(req):
    global dirname
    dirname = os.path.join(os.getcwd(), 'docs')
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req[:3] == 'cat':
        path = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.exists(path):
            with open(path, 'r+') as f:
                line = ''
                for l in f:
                    line+=l
            return line
        else:
            return 'Такого файла не существет'
    elif req[:5] == 'mkdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if not os.path.exists(path):
            os.makedirs(path)
            return f'Папка {req[:5]} создана'
        else: 
            return 'Такая папка уже существет'
    elif req[:5] == 'rmdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if os.path.exists(path):
            shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6::]))
            return f'Папка {req[6::]} удалена'
        else:
            return 'Такой папки не существует'
    elif req[:6]  == 'create':
        req = req.split(' ')
        text = ' '.join(req[2:])
        with open(os.path.join(os.getcwd(), 'docs', req[1]), 'tw', encoding='utf-8') as f:
            f.write(text)
        return 'Файл создан'
    elif req[:6]  == 'remove':
        os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
        return f'Файл {req[7:]} удален'
    elif req[:6]  == 'rename':
        req = req.split(' ')
        os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл переименован'
    elif req[:4]  == 'copy':
        req = req.split(' ')
        shutil.copyfile(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл скопирован'
    elif req[:7] == 'weather':
        try:
            weather = ''
            res = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={req[8:]}&units=metric&lang=ru&APPID=5dad57873e1e11897cd8ced346a8a65d")
            data = res.json()
            for i in data['list']:
               weather += i['dt_txt'] + '{0:+3.0f}'.format(i['main']['temp']) + i['weather'][0]['description'] + '\n'
            return weather 
        except Exception as e:
            return f"Exception (forecast): {e}"
    return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print(f'Просулшиваем порт {PORT}')

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())


conn.close()
