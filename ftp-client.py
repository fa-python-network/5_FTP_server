# coding=utf-8
import logging
import socket
import getpass

logging.basicConfig(filename="client.log", format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Запуск клиента')

def ip():
    while True:
        msg = input('IP сервера (пустая строка = localhost): ')
        if msg == "":  # default
            ip = '127.0.0.1'
            print('IP сервера ' + ip)
        else:
            ip = msg
            print('IP сервера ' + ip)
        break
    logging.info('Установлен ip адресс сервера '+ip)
    return ip


def port():
    while True:
        msg = input('Порт (пустая строка = 9090): ')
        if msg == "":  # default
            port = 9090
            print('Порт 9090')
        else:
            port = int(msg)
            print ('Порт ' + str(port))
        break
    logging.info('Установлен порт ' + str(port))
    return port


HOST = ip()
PORT = port()

print("Добро пожаловать")
while True:
    welcome = input("У вас есть уже аккаунт? y/n: ")
    if welcome == "n":
            sock = socket.socket()
            sock.connect((HOST, PORT))
            print ('Регистрация')
            username = "login" + input("Логин: ")
            password = getpass.getpass('Пароль: ')
            crypt = ''
            for i in password:
                crypt += chr(ord(i) ^ 3)
            password = crypt
            send = username + ':' + password
            sock.send(send.encode())
            response = sock.recv(1024).decode()
            print (response)
            sock.close()
            logging.info('Регистрация пользователя')
            welcome = "y"

    if welcome == "y":
            sock = socket.socket()
            sock.connect((HOST, PORT))
            print ('Вход')
            login1 = 'vhod' + input("Логин: ")
            login2 = getpass.getpass('Пароль: ')
            crypt = ''
            for i in login2:
                crypt += chr(ord(i) ^ 3)
            login2 = crypt
            send = login1 + ':' + login2
            sock.send(send.encode())
            response = sock.recv(1024).decode()
            sock.close()
            if response == 'yes':
                print("Добрый день, " + login1[4:])
                logging.info('Вход юзера')
                break
            logging.error('Неверный логин или пароль')
            print("Неверный логин или пароль.")



print ('Напишите "help", чтобы узнать все команды')
while True:
    request = input('>>> ')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    if request[:4] == 'new ' and request[4:]!='':
        request = request+'^'+input("Вводите тескст для создания файла ")
        sock.send(request.encode())
        logging.info('Создан новый файл на сервере')
    if request[:3] == 'sn ':
        sock.send(request.encode())
        sock.close()
        with open(request[3:], "rb") as f:
            sock = socket.socket()
            sock.connect((HOST, PORT))
            data = f.read()
            sock.sendall(data)
            sock.close()
        sock = socket.socket()
        sock.connect((HOST, PORT))
        sock.send('request'.encode())
        logging.info('Передача файла серверу')
        print ('Файл успешно передан! (Здесь почему то не получилось убрать ошибку с неверной командой)')
    if request[:3] == 'rc ':
        sock.send(request.encode())
        sock.close()
        sock = socket.socket()
        sock.bind(('', PORT+1))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            f = open(request[3:], "wb")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
            f.close()
            break
        sock = socket.socket()
        logging.info('Прем файла с сервера')
        sock.connect((HOST, PORT+2))
        PORT += 2
    else:
        sock.send(request.encode())


    response = sock.recv(2048).decode()
    print(response)

    if request == 'exit':
        logging.info('Остановка клиента')
        break
    sock.close()
