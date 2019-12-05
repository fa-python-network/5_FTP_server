import socket

"""
Это тестовый клиент, он проверяет работоспособность сервера 
Этот клиент не проверяет получение файла от сервера и 
правильность всех случаев регистрации и т. д., т. к. и без них тут много что писать, а цель этого клиента показать 
пример теста 
"""


def send_file(name, sock):
    """Отправялет файл на сервер"""
    sock.send(f'send {name}'.encode())
    with open(name, 'r') as file:
        text = file.read()
    sock.send(str(len(text)).encode())
    sock.send(text.encode())
    return


def new_user(name, sock):
    sock.send(name.encode())
    flag = sock.recv(1024).decode()
    if int(flag):
        password = '12'
        sock.send(password.encode())
    else:
        flag2 = 1
        sock.send(str(flag2).encode())
        old_user(name, sock)


def old_user(name, sock):
    sock.send(name.encode())
    # Если 1 - имя есть, если 0 - это имя ещё не зарегестрированно
    flag = sock.recv(1024).decode()
    if int(flag):
        password = '12'
        sock.send(password.encode())
        flag = sock.recv(1024).decode()


def login(sock):
    sock.send('1'.encode())
    new_user('Test', sock)


def testing():
    HOST = '127.0.0.1'
    PORT = 9090

    sock = socket.socket()
    sock.connect((HOST, PORT))
    print(f"Присоединились к {HOST} {PORT}")

    login(sock)  # Регистрируем нового пользователя
    # Проверка приветствия
    data = (sock.recv(1024).decode())
    if data != 'Hello, Test':
        return "Ошибка в создании нового пользователя"

    # pwd
    request = 'pwd'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "\\Test":
        return "Ошибка в pwd"

    # mkdir
    request = 'mkdir testdir'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "папка testdir успешно создана":
        return "Ошибка в mkdir"

    # ls
    request = 'ls'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "testdir":
        return "Ошибка в ls"

    # cd
    request = 'cd testdir'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "Текущая директория \\Test\\testdir":
        return "Ошибка в cd"
    request = 'pwd'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "\\Test\\testdir":
        return "Ошибка в cd"

    # send
    request = 'send main.txt'
    send_file(request.split()[1], sock)
    answer = sock.recv(1024).decode()
    if answer != "получен файл main.txt":
        return "Ошибка в send"

    # size
    request = 'send main2.txt'
    send_file(request.split()[1], sock)
    answer = sock.recv(1024).decode()
    if answer != "Недостаточно места на диске":
        return "Ошибка в выделении места на диске"

    # cd ..
    request = 'cd ..'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "Текущая директория \\Test":
        print(answer)
        return "Ошибка в cd.."

    # rmdir
    request = 'rmdir testdir'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "папка testdir успешно удалена":
        return "Ошибка в rmdir"

    # exit
    sock.close()
    return "Миша - лучший программист"


print(testing())
