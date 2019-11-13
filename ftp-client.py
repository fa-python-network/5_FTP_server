import socket
from logger import Logfile
import pickle
import os
import time


HOST = 'localhost'
try:
    port=int(input("Ваш порт:"))
    if not 0 <= port <= 65535:
        raise ValueError
except ValueError :
    port = 9090

status=True
s=True
while status:
    sock = socket.socket()
    sock.connect((HOST, port))
    l=Logfile()
    l.serverstart()
    menu='Здравствуйте!\nВам доступны следующие функции: \n1)ls  - показывает содержимое доступной вам директории \n2)mkdir <filename> - создание папки  \n4)rm <filename> - удалеяет папкy \n5)delete <filename> - удаляет файл \n6)rename <filename> <new name> - переименовывает файл/директорию в <new name>\n7)exit - отключение клиента от сервера\n8)copy.from <from> <filename> - копирует файл  с клиента (cl)/сервера (ser) (пример: copy.from cl f.txt)'
    print(menu)
    time.sleep(0.3)
    while s:
        request = input('>')
        #print(response)
        if request == 'exit':
            sock.send(request.encode())
            response = sock.recv(1024).decode()
            print(response)
            status=False
            s=False
        elif request.split()[0] == "copy.from":
            if request.split()[1] == 'cl':
                a=True
                for i in request.split()[2]:
                    if i=='/':
                        print('Название файла указывается без абсолютного пути')
                        a=False
                        break
                if a==True:
                    file = os.path.realpath(request.split()[2])
                    sock.send(f"copy.from cl {file.split('/')[-1]}".encode())
                    time.sleep(0.3)
                    with open(file, "rb") as f:
                        data = f.read(1024)
                        while data:
                            sock.send(data)
                            data = f.read(1024)
                    sock.send(b'sent')
                    print(sock.recv(1024).decode())
            if request.split()[1] == 'ser':
                sock.send(request.encode())
                with open(request.split('/')[-1], "wb") as f:
                    while True:
                        data = sock.recv(1024)
                        if data == b'sent':
                            break
                        f.write(data)
                response = sock.recv(1024).decode()
                print(response)
        else:
            sock.send(request.encode())
            response = sock.recv(1024).decode()
            print(response)
            
    sock.close()