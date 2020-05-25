# coding=utf-8
import shutil
import socket
import os
import logging

logging.basicConfig(filename="server.log", format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Запуск сервера')

def dir_cd(name):
    global dirname
    global d
    global login1
    global num
    global l
    if name == '..':
        try:
            ind = d.pop(0)
            dlina = len(ind) + 1
            dirname = dirname[:-dlina]
            if login1 == 'admin':
                logging.info('Переход в директорию '+dirname[num - l:])
                return dirname[num - l:]
            else:
                logging.info('Переход в директорию '+dirname[num - l:])
                return dirname[num:]
        except:
            logging.info('Попытка ' + login1 + ' выйти за перделы корневой папки')
            return login1 + ', это ваша корневая папка'

    elif name == '':
        d = []
        if login1 == 'admin':
            dirname = os.path.join(os.getcwd())
            logging.info('Переход в корневую директорию ' + dirname[num - l:])
            return dirname[num - l:]
        else:
            dirname = os.path.join(os.getcwd(), 'docs', login1)
            logging.info('Переход в директорию ' + dirname[num - l:])
            return dirname[num:]
    else:
        try:
            r = '; '.join(os.listdir(dirname))
            v = r.find(name)
            if login1 == 'admin' and v != -1:
                d.insert(0, name)
                dirname = os.path.join(dirname, name)
                logging.info('Переход в директорию ' + dirname[num - l:])
                return dirname[num - l:]
            if v != -1:
                d.insert(0, name)
                dirname = os.path.join(dirname, name)
                logging.info('Переход в директорию ' + dirname[num - l:])
                return dirname[num:]
            else:
                return 'Такой директории не существует'
        except:
            logging.error('cd Такой директории не существует')
            return 'Такой директории не существует'



d = ['docs']
len_pr = os.path.join(os.getcwd())
l = len(len_pr.split('/')[-1]) + 6
dirname = os.path.join(os.getcwd(), 'docs')


def process(req):
    global dirname
    global login1
    global d
    global num
    global l
    kor = os.path.join(os.getcwd())
    if req == 'pwd':
        if login1 == 'admin':
            logging.info('pwd ' + dirname[num - l:])
            return dirname[num - l:]
        else:
            logging.info('pwd ' + dirname[num - l:])
            return dirname[num:]
    elif req == 'ls':
        try:
            x = '  '.join(os.listdir(dirname))
            if x != '':
                logging.info('ls ' + x)
                return x
            else:
                logging.info('ls Данная директория пустая')
                return 'Пусто'
        except:
            d = []
            if login1 == 'admin':
                dirname = os.path.join(os.getcwd())
            else:
                dirname = os.path.join(os.getcwd(), 'docs', login1)
            logging.info('ls Неверная директория. Перенаправление в корневую папку')
            return 'Неверная директория. Вы были перенаправлены в корневую папку'
    elif req[:4] == 'cat ':
        try:
            filename = req[4:]
            filename = os.path.join(dirname, filename)
            f = open(filename, 'rt')
            res = f.read()
            f.close()
            logging.info('cat')
            return res
        except:
            logging.error('cat Файла с таким именем не существет')
            return 'Файла с таким именем не существет'
    elif req[:6] == 'mkdir ':
        try:
            dir = req[6:]
            dir = os.path.join(dirname, dir)
            os.mkdir(dir)
            res = 'Директория ' + req[6:] + ' создана'
            logging.info('mkdir '+res)
            return res
        except:
            logging.error('mkdir Невозможно создать директорию с таким именем')
            return 'Невозможно создать директорию с таким именем'
    elif req[:6] == 'rmdir ':
        try:
            dir = req[6:]
            dir = os.path.join(dirname, dir)
            shutil.rmtree(dir)
            res = 'Директория ' + req[6:] + ' удалена'
            logging.info('rmdir ' + res)
            return res
        except:
            logging.error('rmdir Такой директории не существует')
            return 'Такой директории не существует'
    elif req[:3] == 'rm ':
        try:
            filename = req[3:]
            filename = os.path.join(dirname, filename)
            os.remove(filename)
            res = 'Файл ' + req[3:] + ' удален'
            logging.info('rm ' + res)
            return res
        except:
            logging.error('rm Такой файл не существует')
            return 'Такой файл не существует'
    elif req[:4] == 'ref ' and req[4:] != '':
        try:
            filename = req[4:].partition(' ')
            old = os.path.join(dirname, filename[0])
            new = os.path.join(dirname, filename[2])
            os.rename(old, new)
            res = 'Файл переименован.'
            logging.info('ref Файл ' + old + ' переименован в ' + new)
            return res
        except:
            logging.error('ref Такой файл не существует')
            return 'Такой файл не существует'
    elif req[:5] == 'login':
        try:

            dirname = os.path.join(os.getcwd(), 'docs')
            login = req[5:].partition(':')
            username = login[0]
            dir = os.path.join(dirname, username)
            os.mkdir(dir)
            file = open('login/' + username + ".txt", "w")
            file.write(req[5:])
            file.close()
            logging.info('Зарегистрирован пользователь ' + login)
            return 'Пользователь зарегестрирован'
        except:
            logging.error('Попытка зарегистрировать существующего пользователя')
            return 'Такой пользователь существует'
    elif req[:4] == 'vhod':
        try:
            dirname = os.path.join(os.getcwd(), 'docs')
            login = req[4:].partition(':')
            login1 = login[0]
            file = open('login/' + login1 + ".txt", "r")
            data = file.readline()
            file.close()

            if data == req[4:]:
                logging.info('Вход пользователя ' + login1)
                d = []
                if login1 == 'admin':
                    d = ['admin', 'docs']
                dirname = os.path.join(dirname, login1)
                num = dirname.find(login1)
                return 'yes'
            else:
                return 'No'
        except:
            return 'no'
    elif req == 'help':
        f = open(os.path.join(kor, 'help.txt'), 'rt')
        res = f.read()
        f.close()
        logging.info('help page')
        return res
    elif req[:2] == 'cd':
        res = dir_cd(req[3:])
        return res
    elif req[:4] == 'new ' and request[4:] != '':
        text = req[4:].partition('^')
        file = open(os.path.join(dirname, text[0]), "w")
        file.write(text[2])
        file.close()
        logging.info('new создан новый файл ' + os.path.join(dirname, text[0]))
        return 'Файл записан'
    elif req[:3] == 'sn ':
        return 'Файл успешно отправлен'
    elif request[:3] == 'rc ':
        return 'Файл успешно скачан'
    elif req == 'exit':
        logging.info('Клиет '+login1+' отключился от сервера')
        return 'Отключение от сервера...'
    logging.info('Введена несуществующая команда: '+req)
    return 'Такой команды не существует. Напишите help чтобы показать все команды'




def port():
    while True:
        msg = input('Порт (пустая строка = 9090): ')
        if msg == "":  # default
            port = 9090
            print('Порт 9090')
        else:
            port = int(msg)
            print ('Порт ' + str(port))
        break
    return port


PORT = port()


sock = socket.socket()
try:
    sock.bind(('', PORT))
except:
    PORT += 1
    sock.bind(('', PORT))
sock.listen()
logging.info('PORT ' + str(PORT))
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    if request[:3] == 'sn ':
        response = process(request)
        while True:
            conn, addr = sock.accept()
            f = open(os.path.join(dirname, request[3:]), "wb")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
            f.close()
            logging.info('sn отправлен файл на сервер' + os.path.join(dirname, request[3:]))
            break
    elif request[:3] == 'rc ':
        sock.close()
        response = process(request)
        with open(os.path.join(dirname, request[3:]), "rb") as f:
            print("[+] Sending file...")
            sock = socket.socket()
            sock.connect((addr[0], PORT+1))
            data = f.read()
            sock.sendall(data)
            sock.close()
        sock = socket.socket()
        sock.bind(('', PORT+2))
        sock.listen()
        logging.info('rc отправлен файл клиенту' + os.path.join(dirname, request[3:]))
        PORT += 2
        logging.info('PORT смена порта ' + str(PORT))
        print("Смена порта. Прослушиваем порт", PORT)
        conn, addr = sock.accept()

    else:
        response = process(request)

    conn.send(response.encode())

conn.close()
