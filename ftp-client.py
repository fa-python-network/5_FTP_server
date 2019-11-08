import socket
import threading

def send_msg(sock, msg):
    header = f'{len(msg):<4}'
    sock.send(f'{header}{msg}'.encode())


def recv_msg(sock):
    header = int(sock.recv(4).decode().strip())
    data = sock.recv(header*2).decode()
    return data

from time import sleep
sock = socket.socket()
k = False
while not k:
    try:
        print("Host:")
        host = input()
        if host == "":
            host = 'localhost'
        print("Port:")
        port = input()
        if port == "":
            port = 9090

        sock.connect((host, int(port)))

        #Я очень долго пыталась сделать регистрацию пользователей
        #И в итоге пришла к выводу, что проще их написать ручками
        #Поэтому просто проверяю пользователя в файле
        print("Введите свое Имя")
        msg = input()
        send_msg(sock, msg)
        proverka = recv_msg(sock)
        while proverka == 'False':
            print("Такого пользователя не существует \nВведите свое имя")
            msg = input()
            send_msg(sock, msg)
            proverka = recv_msg(sock)

        #проверяем пароль
        print("введите пароль")
        psw = str(input())
        send_msg(sock, psw)
        proverka = recv_msg(sock)
        while proverka == 'False':
            print("Неверный пароль \nВведите пароль")
            psw = str(input())
            send_msg(sock, psw)
            proverka = recv_msg(sock)

        request = ''
        while request != 'exit':
            request = input('>')

            send_msg(sock, request)

            response = recv_msg(sock)
            print(response)

        k = True
    except KeyboardInterrupt:
        sock.close()