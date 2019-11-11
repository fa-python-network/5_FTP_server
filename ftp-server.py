import socket
import os
import requests
import json
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''



def process(req):
    global dirname
    dirname = os.path.join(os.getcwd(), 'docs')
    print(dirname)
    weath = ''
    if req == 'pwd':
        return dirname

    elif req == 'ls':
         return '; '.join(os.listdir(dirname))

    elif req[:5] == "mkdir":
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if not os.path.exists(path):
            os.makedirs(path)
            return f"Папка {req[6:]} создана"
        else:
            return "Такая папка уже существует"

    elif req[:5] == 'rmdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                return f"Папка {req[6:]} удалена"
            return 'это файл, а не директория'
        else:
            return "Такой папки и не существуетвовало"

    elif req[:3] == 'cat':
        path = os.path.join(os.getcwd(), 'docs', req[4:])
        if os.path.exists(path):
            with open(path, 'r+') as f:
                line = ''
                for l in f:
                    line += l
            return line
        else:
            return 'Такого файла не существет'

    elif req[:6] == 'create':
        req = req.split(' ')
        if os.path.exists(f"{dirname}/{req[1]}"):
            return 'Такой уже есть'
        text = ' '.join(req[2:])
        with open(os.path.join(os.getcwd(), 'docs', req[1]), 'tw', encoding='utf-8') as f:
            f.write(text)
        return 'Файл создан'

    elif req[:6] == 'remove':
        if os.path.exists(f'{dirname}/{req[7:]}'):
            if os.path.isfile:
                os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
                return f'Файл {req[7:]} удален'
            return 'Это директория, а не файл'
        else:
            return 'такого файла не было'

    elif req[:6] == 'rename':
        req = req.split(' ')
        if os.path.exists(f'{dirname}/{req[1]}'):
            os.rename(os.path.join(f'{dirname}/{req[1]}'), os.path.join(f'{dirname}/{req[2]}'))
            return 'Файл переименован'
        return 'такого файла не было'

    elif req[:4] == 'copy':
        req = req.split(' ')
        if os.path.exists(f'{dirname}/{req[1]}'):
            shutil.copyfile(os.path.join(f'{dirname}/{req[1]}'), os.path.join(f'{dirname}/{req[2]}'))
            return 'Файл скопирован'
        return 'файла не существует'

    elif req[:7] == 'weather':
        appid = '24c25a726b2b305c6bbbc39faf1370ac'
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast?",
                               params={'q': req[8:], 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            for i in data['list']:
                weath += i['dt_txt'] + '{0:+3.0f}'.format(i['main']['temp']) + i['weather'][0]['description'] + '\n'
            return weath
        except Exception as e:
            print("Exception (forecast):", e)
            pass
    return 'bad request'



PORT = 6666

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
