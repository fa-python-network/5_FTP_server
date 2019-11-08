import socket
import os
import threading
import json

sock = socket.socket()
online_users = []



def read_file(name):
    try:
        testFile = open(name)
        content = testFile.read()
        testFile.close()
        return content
    except FileNotFoundError:
        return "нет такого файла"



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
        data = conn.recv(header*2).decode()
        return data
    except (ValueError, ConnectionAbortedError):
        return


class T(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.dir = ''
            #os.path.join(os.getcwd(), login)
        self.now_dir = ''
            #os.path.join(os.getcwd(), login)

    def run(self):

#Проверка имени

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


#Проверка пароля

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


        #сейчас задаим текущую директорию и директорию, из которой не может уходить пользователь
        self.dir = os.path.join(os.getcwd(), name)
        self.now_dir = os.path.join(os.getcwd(), name)


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
                        send_msg(self.conn,read_file(os.path.join(self.now_dir, request.split(' ')[1])))
                    except IndexError:
                        send_msg(self.conn,"нет такого файла или необходимо изменить директорию")

                else:
                    send_msg(self.conn,'bad request')
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
