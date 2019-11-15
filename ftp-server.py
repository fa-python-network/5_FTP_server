import socket
import os
import requests
import json
import shutil


def process(urequest):
    global dirname
    dirname = os.path.join(os.getcwd(), 'docs')
    if urequest == 'pwd':
        return dirname
    elif urequest == 'ls':
        return '; '.join(os.listdir(dirname))
    elif urequest[:3] == 'cat':
        path = os.path.join(os.getcwd(), 'docs', urequest[4::])
        if os.path.exists(path):
            with open(path, 'r+') as f:
                line = ''
                for l in f:
                    line += l
            return line
        else:
            return 'Такого файла не существет'
    elif urequest[:5] == 'mkdir':
        path = os.path.join(os.getcwd(), 'docs', urequest[6::])
        if not os.path.exists(path):
            os.makedirs(path)
            return f'Папка {urequest[:5]} создана'
        else: 
            return 'Такая папка уже существет'
    elif urequest[:5] == 'rmdir':
        path = os.path.join(os.getcwd(), 'docs', urequest[6::])
        if os.path.exists(path):
            shutil.rmtree(os.path.join(os.getcwd(), 'docs', urequest[6::]))
            return f'Папка {urequest[6::]} удалена'
        else:
            return 'Такой папки не существует'
    elif urequest[:6] == 'create':
        urequest = urequest.split(' ')
        text = ' '.join(urequest[2:])
        with open(os.path.join(os.getcwd(), 'docs', urequest[1]), 'tw', encoding='utf-8') as f:
            f.write(text)
        return 'Файл создан'
    elif urequest[:6]  == 'remove':
        os.remove(os.path.join(os.getcwd(), 'docs', urequest[7:]))
        return f'Файл {urequest[7:]} удален'
    elif urequest[:6]  == 'rename':
        urequest = urequest.split(' ')
        os.rename(os.path.join(os.getcwd(), 'docs', urequest[1]), os.path.join(os.getcwd(), 'docs', urequest[2]))
        return 'Файл переименован'
    elif urequest[:4]  == 'copy':
        urequest = urequest.split(' ')
        shutil.copyfile(os.path.join(os.getcwd(), 'docs', urequest[1]), os.path.join(os.getcwd(), 'docs', urequest[2]))
        return 'Файл скопирован'
    elif urequest[:7] == 'weather':
        try:
            weather = ''
            res = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={urequest[8:]}&units=metric&lang=ru&APPID=5dad57873e1e11897cd8ced346a8a65d")
            data = res.json()
            for i in data['list']:
               weather += i['dt_txt'] + '{0:+3.0f}'.format(i['main']['temp']) + i['weather'][0]['description'] + '\n'
            return weather 
        except Exception as e:
            return f"Exception (forecast): {e}"
    return 'bad request'


PORT = 9090

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
