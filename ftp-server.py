import socket
import os
import threading
import json

sock = socket.socket()
online_users = []


def is_it_path(st):
    if os.name == 'posix':
        if st.find('/') == -1:
            return True
        else:
            return False
    elif os.name == 'nt':
        if st.find('\\') == -1:
            return True
        else:
            return False


def read_file(name):
    try:
        testFile = open(name)
        content = testFile.read()
        testFile.close()
        return content
    except FileNotFoundError:
        return "нет такого файла"


def echo(st, now_dir):
    try:
        if len(st.split(' >> ')) == 2:
            new_st = st.split(' >> ')
            new_st[1] = os.path.join(now_dir, new_st[1])
            file = open(new_st[1], 'a')
            file.write('\n')
            file.write(new_st[0])
            file.close()
            return f'текс записан в файл {new_st[1]}'

        elif len(st.split(' > ')) == 2:
            new_st = st.split(' > ')
            new_st[1] = os.path.join(now_dir, new_st[1])
            file = open(new_st[1], 'w')
            file.write('\n')
            file.write(new_st[0])
            file.close()
            return f'текс записан в файл {new_st[1]}'
        else:
            return 'Неверный формат ввода'
    except FileNotFoundError:
        return 'Неверный формат ввода'


def mkdir(st, now_dir):
    if st[0] == ' ':
        return ('неверный формат ввода')
    else:
        try:
            os.makedirs(os.path.join(now_dir, st))

            return os.path.join(now_dir, st)
        except OSError:
            return ('папка уже существует')


def rm(st, now_dir):
    if st[0] == ' ':
        return ('неверный формат ввода')
    else:
        try:
            os.remove(os.path.join(now_dir, st))
            return os.path.join(now_dir, st)
        except FileNotFoundError:
            return ('такого файла не существует')
        except PermissionError:
            return ('Отказано в доступе')


def rmdir(st, now_dir):
    if st[0] == ' ':
        return ('неверный формат ввода')
    else:
        try:
            os.rmdir(os.path.join(now_dir, st))
            return os.path.join(now_dir, st)
        except FileNotFoundError:
            return ('папки не существует')


def cd(st, now_dir):
    if st == '..':
        now_dir = os.path.split(now_dir)[0]
        return (now_dir)
    elif st[0] == ' ' or st[len(st) - 1] == ' ':
        return ('неверный формат ввода')
    elif os.path.exists(os.path.join(now_dir, st)):
        if is_it_path(st):
            return os.path.join(now_dir, st)
        else:
            'нельзя вводить путь'
    else:
        return 'директории не существует'


##'users.json'
def write_into_json(dct, file_name):
    with open(file_name, 'w') as f:
        json.dump(dct, f)


def read_from_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def send_msg(conn, msg):
    try:
        header = f'{len(msg):<4}'
        conn.send(f'{header}{msg}'.encode())
    except ConnectionAbortedError:
        pass


def recv_msg(conn):
    try:
        header = int(conn.recv(4).decode().strip())
        data = conn.recv(header * 2).decode()
        return data
    except (ValueError, ConnectionAbortedError):
        return


class T(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.dir = ''
        # os.path.join(os.getcwd(), login)
        self.now_dir = ''
        # os.path.join(os.getcwd(), login)

    def run(self):

        # Проверка имени

        name = recv_msg(self.conn)
        pr = True
        try:
            ex_name = users[name]
        except KeyError:
            pr = False
        send_msg(self.conn, str(pr))
        while not pr:
            name = recv_msg(self.conn)
            pr = True
            try:
                ex_name = users[name]
            except KeyError:
                pr = False
            send_msg(self.conn, str(pr))

        # Проверка пароля

        pr = False
        pswd = recv_msg(self.conn)
        if ex_name == pswd:
            pr = True
        send_msg(self.conn, str(pr))
        while not pr:
            pswd = recv_msg(self.conn)
            if ex_name == pswd:
                pr = True
            send_msg(self.conn, str(pr))

        # сейчас задаим текущую директорию и директорию, из которой не может уходить пользователь
        self.dir = os.path.join(os.getcwd(), name)
        self.now_dir = os.path.join(os.getcwd(), name)
        mkdir(name, os.getcwd())


        while True:
            request = recv_msg(self.conn)
            print(request)

            if request:
                if request == 'pwd':
                    send_msg(self.conn, self.now_dir)
                elif request == 'ls':
                    send_msg(self.conn, '; '.join(os.listdir(self.now_dir)))
                # cat работает только для файлов, которые находятся в текущей папке
                # НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ ПУТЬ К ФАЙЛУ ДЛЯ ЭТОГО
                elif request.split(' ')[0] == 'cat':
                    try:
                        send_msg(self.conn, read_file(os.path.join(self.now_dir, request.split(' ')[1])))
                    except IndexError:
                        send_msg(self.conn, "нет такого файла или необходимо изменить директорию")

                # нельзя создавать пустой фай через echo
                elif request[:5] == 'echo ':
                    send_msg(self.conn, echo(request[5:], self.now_dir))

                # mkdir, rm, rmdir работает только для файлов и директорий, которые находятся в текущей папке
                # НЕЛЬЗЯ ИСПОЛЬЗОВАТЬ ПУТЬ К ФАЙЛУ ДЛЯ ЭТОГО
                elif request[:6] == 'mkdir ':
                    if is_it_path(request[6:]):
                        self.now_dir = mkdir(request[6:], self.now_dir)
                        send_msg(self.conn, self.now_dir)
                    else:
                        send_msg(self.conn, 'нельзя вводить путь')

                elif request[:3] == 'rm ':
                    if is_it_path(request[3:]):
                        send_msg(self.conn, rm(request[3:], self.now_dir))
                    else:
                        send_msg(self.conn, 'нельзя вводить путь')

                elif request[:6] == 'rmdir ':
                    if is_it_path(request[:6]):
                        send_msg(self.conn, rmdir(request[6:], self.now_dir))
                    else:
                        send_msg(self.conn, 'нельзя вводить путь')

                elif request[:3] == 'cd ':
                    if (self.now_dir == self.dir and request[3:] != '..') or (self.now_dir != self.dir):
                        x = cd(request[3:], self.now_dir)
                        if x != 'неверный формат ввода' or x != 'директории не существует' or x != 'нельзя вводить путь':
                            self.now_dir = x
                            send_msg(self.conn, self.now_dir)
                        else:
                            send_msg(self.conn, x)
                    elif (self.now_dir == self.dir and request[3:] == '..'):
                        send_msg(self.conn, 'Ну и куда ты пытаешься выйти?')


                else:
                    send_msg(self.conn, 'bad request')
            elif request is None:
                break

            else:
                send_msg(self.conn, 'bad request')

        self.conn.close()


port = 9090
users = read_from_json('users.json')
try:
    sock.bind(('', port))
except OSError:
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    print(f"use port {port}")
sock.listen()
while True:
    conn, addr = sock.accept()
    print(addr)
    T(conn, addr).start()
