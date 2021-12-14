import socket
import config
import os

while True:
    request = input('>')
    sock = socket.socket()
    sock.connect((config.HOST_ADDR, config.PORT))

    if request.split()[0] == 'sendfile':
        filename = request.split()[1]
        sock.send(f"getfile {filename} ".encode())
        with open(os.path.join('docs', 'client', filename), 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                sock.send(bytes_read)
                if len(bytes_read) < 1024:
                    break
    elif request.split()[0] == 'getfile':
        filename = request.split()[1]
        sock.send(f"sendfile {filename}".encode())
        with open(os.path.join('docs', 'client', filename), 'wb') as f:
            while True:
                bytes_read = sock.recv(1024)
                f.write(bytes_read)
                if len(bytes_read) < 1024:
                    break
    else:
        sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    if response == config.INTERRUPT_MESSAGE:
        sock.close()
        break

    sock.close()