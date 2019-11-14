import shutil

"""
pwd - сервер вернёт название рабочей директории
ls - сервер вернёт список файлов в рабочей директории
cat - сервер вернёт содержимое файла
mkdir - сервер создаёт директорию с указанным именем
rmdir - сервер удаляет директорию с указанным именем
rm - сервер удаляет файл с указанным именем
touch - сервер создаёт файл с указанным именем
rename - сервер переименновывает файл с указанным именем 
send - сервер ПОЛУЧАЕТ файл от клинета
recv - сервер ОТПРАВЛЯЕТ файл клинету
(называть команды такими именами удобнее для клиента)
"""


def pwd():
    return os.getcwd()


def ls():
    return ' '.join(os.listdir(os.getcwd()))


def mkdir(name):
    path = pwd() + '/' + name
    os.mkdir(path)
    return f'папка {name} успешно создана'


def rmdir(name):
    path = pwd() + '/' + name
    shutil.rmtree(path)
    return f'папка {name} успешно удалена'


def rm(name):
    path = pwd() + '/' + name
    os.remove(path)
    return f'файл {name} успешно удалён'


def touch(name):
    with open(name, 'w') as file:
        pass
    return f'файл {name} успешно создан'


def rename(name1, name2):
    os.rename(name1, name2)
    return f'файл {name1} успешно переименнован в {name2}'


def send(name, conn):
    length = conn.recv(1024).decode()
    text = conn.recv(int(length)).decode()
    with open(name, 'w') as file:
        file.write(text)
    return f'получен файл {name}'


def recv(name, conn):
    with open(name, 'r') as file:
        text = file.read()
    conn.send(str(len(text)).encode())
    conn.send(text.encode())
    return f'отправлен файл {name}'


def process(req, args=None):
    f = commands[req]
    if args:
        return f(*args)
    return f()


commands = {'pwd': pwd, 'ls': ls, 'mkdir': mkdir, 'rmdir': rmdir, 'rm': rm, 'touch': touch, 'rename': rename,
            'send': send, 'recv': recv}

PORT = 9090

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print(f"Слушаем порт {PORT}")

while True:
    conn, addr = sock.accept()
    print(addr)
    while True:

        request = conn.recv(1024).decode()
        request = request.split()
        if not request:
            break
        func = request[0]
        if len(request) > 0:
            args = request[1:]
        else:
            args = None
        if args:
            if func in ['send', 'recv']:
                args.append(conn)
            response = process(func, args)
        else:
            response = process(func)
        conn.send(response.encode())
    conn.close()

sock.close()
