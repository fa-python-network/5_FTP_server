import socket
import os

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''


def process(req):
    try:
        if req == 'pwd':
            return os.path.relpath(os.getcwd(), startdir)
        elif req == 'ls':
            return '; '.join(os.listdir())
        elif 'cat' in req:
            file = req.split()[-1]
            with open(file) as f:
                return f.read()
        elif 'mkdir' in req:
            dirname = req.split()[-1]
            os.mkdir(dirname)
            return 'Success'
        elif 'chdir' in req:
            dirname = req.split()[-1]
            os.chdir(dirname)
            return 'Success'
        return 'bad request'
    except Exception as e:
        return e


def receive(conn):
    count = int(conn.recv(4).decode())
    return conn.recv(count).decode()


def send(conn, message):
    message = message[:1020]
    count = len(message)
    conn.send('{:4}{}'.format(count, message).encode())


PORT = 6667

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)
os.chdir('docs')
startdir = os.getcwd()

try:
    while True:
        conn, addr = sock.accept()
        send(conn, 'Welcome, what\'s your name?')
        name = receive(conn)
        try:
            os.mkdir(name)
        except:
            pass
        os.chdir(name)
        send(conn, 'Welcome, {}'.format(name))
        while True:
            try:
                req = receive(conn)
                resp = process(req)
                send(conn, resp)
            except:
                conn.close()
finally:
    sock.close()
