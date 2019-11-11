#-*-coding:cp1251-*-
from  socket import socket, AF_INET, SOCK_STREAM


def recv(conn):
    header = conn.recv(5)  # сколько принимаем
    # try:
    header = int(header.decode('cp1251'))
    message = conn.recv(header).decode('cp1251')
    return message
# except:
#     print('Клиент отключился')


def send(conn, message):
    header = len(message)
    full_message = f'{header:5}{message}'.encode('cp1251')
    conn.send(full_message)


sock = socket(AF_INET, SOCK_STREAM)
port = int(input('port'))
host = input('host')
sock.connect(('localhost', port))
while True:
    msg = recv(sock)
    print(msg)
    result = input('>')
    send(sock, result)





