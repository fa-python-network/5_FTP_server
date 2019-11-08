import socket
import threading
import os

dirname = os.path.join(os.getcwd(), 'docs')


def read_file(name):
    try:
        testFile = open(name)
        content = testFile.read()
        testFile.close()
        return content
    except FileNotFoundError:
        return "нет такого файла"


# def ch_dir(path):
# ls1 = path.split('/')
# ls2 = path.split(f"/\")
# if ls1 < l2:
# ls

def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req.split(' ')[0] == 'cat':
        try:
            return read_file(os.path.join(dirname, req.split(' ')[1]))
        except IndexError:
            return ("нет такого файла или необходимо изменить директорию")

    return 'bad request'


PORT = 9095

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
