import socket
from logger import Logfile
import pickle
import os
import time
import sys
from threading import Thread
from time import sleep
from getpass import getpass
status = None


def rcv():
    global status
    while status != "finish":
        try:
            global sock
            global data
            data = sock.recv(1024)
            if not data:
                sys.exit(0)
            try:
                s = pickle.loads(data)[0]
                if s == "finish":
                    sock.close()
                    status = "finish"
                    break
                status = s
                data = pickle.loads(data)[1]
            except:
                print(data.decode())
        except OSError:
            r = 'не робит'
            print(r)


def auth():
    name = input(data)
    sock.send(pickle.dumps(["auth", name]))
    sleep(1.5)


def nameRequest(name):
    sock.send(pickle.dumps(["nameRequest", name]))
    sleep(1.5)


def sendPasswd():
    passwd = getpass(data)
    sock.send(pickle.dumps(["passwd", passwd]))
    sleep(1.5)


def success():
    print(data)
    path = str(os.getcwd())+'/'+l
    
    os.chdir(path)
    log=Logfile()
    log.serverstart(l)
    
    global status
    status = 'ready'


HOST = 'localhost'
try:
    port = int(input("Ваш порт:"))
    if not 0 <= port <= 65535:
        raise ValueError
except ValueError:
    port = 9090


st = True
s = True
while st:
    sock = socket.socket()
    sock.connect((HOST, port))
    menu = 'Здравствуйте!\nВам доступны следующие функции: \n1)ls  - показывает содержимое доступной вам директории \n2)mkdir <filename> - создание папки  \n4)rm <filename> - удалеяет папкy \n5)delete <filename> - удаляет файл \n6)rename <filename> <new name> - переименовывает файл/директорию в <new name>\n7)exit - отключение клиента от сервера\n8)copy.from <from> <filename> - копирует файл  с клиента (cl)/сервера (ser) (пример: copy.from cl f.txt)'
    print(menu)
    Thread(target=rcv).start()

    while status != 'finish':
        if status:
            if status == "auth":
                auth()
            elif status == "passwd":
                sendPasswd()
            elif status == "success":
                success()
            elif status == "nameRequest":
                l = input('Логин: ')
                nameRequest(l)

            else:

                sleep(0.5)
                request = input('>')
                if request == "exit":
                    sock.send(request.encode())
                    
                    status = "finish"
                    st=False
                    break
                elif request.split()[0] == "copy.from":
                    if request.split()[1] == "-ser":
                        sock.send(request.encode())
                        with open(request.split('/')[-1], "wb") as f:
                            while True:
                                data = sock.recv(1024)
                                if data == b"sent":
                                    break
                                f.write(data)
                    else:
                        a = True
                        path = os.getcwd()
                        t=path.split('/')[-1]
                        r = os.path.realpath(request.split()[2])
                        r=r.split('/')[-2]
                        if r != t:
                                print('Отказано в доступе')
                                a = False
                                break
                        if a == True:
                            file = os.path.realpath(request.split()[2])
                            sock.send(f"copy.from cl {file.split('/')[-1]}".encode())
                            sleep(0.5)
                            with open(file, "rb") as f:
                                data = f.read(1024)
                                while data:
                                    sock.send(data)
                                    data = f.read(1024)
                                sleep(0.5)
                                sock.send(b"sent")
                else:
                    
                    sock.send(request.encode())