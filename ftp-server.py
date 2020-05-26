import socket
import os

current_dir = 'home'


def process(req):
    print(req)
    if req == 'pwd':
        return current_dir
    if req == 'ls':
        res = os.listdir('./home/')
        return ':'.join(res)
    if req[:4] == 'cat':
        filename = req[4:]
        print(filename)
        try:
            f = open(filename, 'rt')
            res = f.read()
            f.close()
        except FileNotFoundError:
            return 'File not found'
        return res
    return 'Default response'


PORT = 780

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

print("Прослушать порт ", PORT)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    response = process(request)
    conn.send(response.encode())
    conn.close()
