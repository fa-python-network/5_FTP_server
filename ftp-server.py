import os
from json import load
from socket import AF_INET, SOCK_STREAM
import threading
import socket


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
        else:
            send(conn, m)



sock = socket.socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print("Прослушиваем порт", sock.getsockname()[1])

while True:
    conn, addr = sock.accept()
    threading.Thread(target = handle_client, args = [conn]).start()
