from socket import socket, AF_INET, SOCK_STREAM


def recv(conn):
    header = conn.recv(5)
    header = int(header.decode())
    message = conn.recv(header).decode('windows-1251')
    return message


def send(conn, message):
    header = len(message)
    full_message = f'{header:5}{message}'.encode('windows-1251')
    conn.send(full_message)


sock = socket(AF_INET, SOCK_STREAM)
host = input('host: ')
port = int(input('port: '))
sock.connect(('localhost', port))
while True:
    msg = recv(sock)
    print(msg)
    request = input('')
    send(sock, request)
    if request == 'exit':
        sock.close()
        break
