#-*-coding:cp1251-*-
import os
import threading
from  socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from json import load, dump

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')



host = input('Введите хост') or 'localhost'
port = input('Введите порт') or '0'
port = int(port)


def recv(conn):
     header = conn.recv(5) #сколько принимаем
     try:
         header = int(header.decode('cp1251'))
         message = conn.recv(header).decode('cp1251')
         return message
     except:
         print('Клиент отключился')

def send(conn, message):
    header = len(message)
    full_message = f'{header:5}{message}'.encode('cp1251')
    conn.send(full_message)


def handle_client(conn):
    auth(conn)
    while 1:
        received_msg = recv(conn)
        if not received_msg:
            conn.close()
            return
        if received_msg == 'pwd':
            send(conn, dirname)
        elif received_msg == 'ls':
            send(conn, '; '.join(os.listdir(dirname)))
        elif received_msg.startswith('cat'):
            file = received_msg.split()[-1]
            with open(f'docs/{file}') as f:
                send(conn,f.read())
        else:
            send(conn, received_msg)


def auth(conn: socket):
    send(conn, 'Введите логин')
    login = recv(conn)
    send(conn, 'Введите пароль')
    password = recv(conn)
    with open("auth.json", "r") as file:
        a = load(file)
    if login in a and a[login] == password:
        send(conn,'Аутентификация прошла успешно!')
        return login
    else:
        send(conn, 'Аутентификация не пройдена. Повторите.')





sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print("Прослушиваем порт", sock.getsockname()[1])

while True:
    conn, addr = sock.accept()
    threading.Thread(target = handle_client, args = [conn]).start()
