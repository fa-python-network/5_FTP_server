import socket


def send_file(name, sock):
    """Отправялет файл на сервер"""
    sock.send(f'send {name}'.encode())
    with open(name, 'r') as file:
        text = file.read()
    sock.send(str(len(text)).encode())
    sock.send(text.encode())
    return


def recv_file(name, sock):
    """Получает файл от сервера"""
    length = sock.recv(1024).decode()
    text = sock.recv(int(length)).decode()
    with open(name, 'w') as file:
        file.write(text)
    return


def new_user(name):
    sock.send(name.encode())
    # Проверка незанятости данного имени 1 - свободно, 0 - занято.
    flag = sock.recv(1024).decode()
    if int(flag):
        while True:
            print("Введите пароль")
            password = input()
            print("Повторите пароль")
            password2 = input()
            if password == password2:
                break
        sock.send(password.encode())
    else:
        print("Данное имя уже занято")
        print("Чтобы войти под этим именем введите 1")
        print("Чтобы ввести другое имя введите 0")
        flag2 = int(input())
        sock.send(str(flag2).encode())
        if flag2:
            old_user(name)
        else:
            name = input("Введите ваше имя: ")
            new_user(name)


def old_user(name):
    sock.send(name.encode())
    # Если 1 - имя есть, если 0 - это имя ещё не зарегестрированно
    flag = sock.recv(1024).decode()
    if int(flag):
        while True:
            password = input("Введите пароль: ")
            sock.send(password.encode())
            flag = sock.recv(1024).decode()
            if not int(flag):
                break
    else:
        print("Такого имени не существует")
        print("Для регистрации под этим именем введите 1")
        print("Чтобы ввести другое имя введите 0")
        flag2 = input()
        sock.send(flag2.encode())
        if int(flag2):
            new_user(name)
        else:
            name = input("Введите ваше имя: ")
            old_user(name)


def login():
    # Регистрация или Вход в акк
    print("Привет :)")
    print("Для регистрации введите 'R'")
    print("Для авторизации введите 'L'")
    while True:
        data = input()
        if data == 'R':
            sock.send('1'.encode())
            print("Введите ваше имя: ")
            name = input()
            new_user(name)
            break
        elif data == 'L':
            sock.send('0'.encode())
            name = input('Введите ваше имя: ')
            old_user(name)
            break
        else:
            print("Попробуйте ещё раз")


HOST = '127.0.0.1'
PORT = 9090

sock = socket.socket()
sock.connect((HOST, PORT))
print(f"Присоединились к {HOST} {PORT}")

login()
print(sock.recv(1024).decode())

while True:
    request = input()
    if request == 'exit':
        break
    elif request.split()[0] == 'send':
        send_file(request.split()[1], sock)
    elif request.split()[0] == 'recv':
        recv_file(request.split()[1], sock)
    else:
        sock.send(request.encode())

    answer = sock.recv(1024).decode()
    print(answer)

sock.close()
