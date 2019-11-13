import socket


def receive(sock):
    count = int(sock.recv(4).decode())
    return sock.recv(count).decode()


def send(sock, message):
    message = message[:1020]
    count = len(message)
    sock.send('{:4}{}'.format(count, message).encode())


host, port = input('Host:Port\n').split(':')
port = int(port)
sock = socket.socket()
sock.connect((host, port))
while True:
    msg = receive(sock)
    print(msg)
    command = input('>')
    if command == 'exit':
        break
    send(sock, command)
sock.close()
