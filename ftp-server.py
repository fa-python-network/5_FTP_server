import os
from json import load
from socket import AF_INET, SOCK_STREAM
import threading
import socket
import shutil


'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''
host = input('HOST: ') or 'localhost'
port = input('PORT: ') or '0'
port = int(port)

dirname = os.path.join(os.getcwd(), 'docs')


def recv(conn):
    header = conn.recv(5)
    try:
        header = int(header.decode('windows-1251'))
        message = conn.recv(header).decode('windows-1251')
        return message
    except:
        print('Отключение клиента')


def send(conn, message):
    header = len(message)
    full_message = f'{header:5}{message}'.encode('windows-1251')
    conn.send(full_message)


def auth(conn: socket):
    send(conn, 'Введите логин')
    login = recv(conn)
    send(conn, 'Введите пароль')
    password = recv(conn)
    with open("База.json", "r") as file:
        a = load(file)
    if login in a and a[login] == password:
        send(conn, 'OK')
        return login
    else:
        send(conn, 'Неправильное имя пользователя или пароль')


def handle_client(conn):
    auth(conn)
    while 1:
        m = recv(conn)
        if not m:
            conn.close()
            return
        if m == 'pwd':
            send(conn, dirname)

        elif m == 'ls':
            send(conn, '; '.join(os.listdir(dirname)))

        elif m.startswith('cat'):
            file = m.split()[-1]
            with open(f'docs/{file}') as f:
                send(conn, f.read())

        elif m.startswith('mkdir'):
            path = os.path.join(os.getcwd(), 'docs', m[6:])
            if not os.path.exists(path):
                os.makedirs(path)
                send(conn, f'Папка {m[6:]} создана')
            else:
                send(conn, 'tакая папка уже существет')

        elif m.startswith('rmdir'):
            path = os.path.join(os.getcwd(), 'docs', m[6:])
            if os.path.exists(path):
                os.rmdir(path)
                send(conn, f'Папка {m[6:]} удалена')
            else:
                send(conn, 'Такой папки не существует')

        elif m.startswith('create'):
            file = os.path.join(os.getcwd(), 'docs', m[7:])
            if not os.path.isfile(file):
                f = open(file, 'w')
                f.close()
                send(conn, 'Файл создан')
            else:
                send(conn, 'Такой файл уже существует')

        elif m.startswith('remove'):
            file = os.path.join(os.getcwd(), 'docs', m[7::])
            if os.path.isfile(file):
                os.remove(file)
                send(conn,"Файл удален")
            else:
                send(conn,"нет такого файла")

        elif m.startswith('rename'):
                m=m.split()
                file = os.path.join(os.getcwd(), 'docs', a[1])
                if os.path.isfile(file):
                    os.rename(os.path.join(os.getcwd(), 'docs', a[1]), os.path.join(os.getcwd(), 'docs', a[2]))
                    send(conn, "Файл переименован")
                else:
                    send(conn,"Нет файла")
        elif m.startswith('send'):
                s = os.path.join(os.getcwd(), 'docs', m[5::])
                try:
                    shutil.copy(s, os.getcwd())
                    send(conn,"The file was copied to the server")
                except:
                    send(conn,"There's no such file in the directory")

        elif m.startswith('get'):
            s = os.path.join(os.getcwd(), 'docs')
            a = os.path.join(os.getcwd(), m[4::])
            try:
                shutil.copy(a, s)
                send(conn,"The file was copied from the server")
            except:
                send(conn,"There's no such file on the server")

        else:
            send(conn, 'Command is not founded')

sock = socket.socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print("Прослушиваем порт", sock.getsockname()[1])

while True:
    conn, addr = sock.accept()
    threading.Thread(target = handle_client, args = [conn]).start()
