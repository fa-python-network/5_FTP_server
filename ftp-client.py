import socket
import os
import pickle
import sys
from time import sleep
from getpass import getpass
from threading import Thread
HOST = 'localhost'

class Client:

    '''
    реализация init
    '''
    def __init__(self, port = 9090, status = None):
        self.sock = socket.socket()
        self.port = int(input("Введите порт:"))
        self.name = input("Введите Ваше имя: ")
        self.status = status
        self.sock.connect((HOST, self.port))
        Thread(target=self.recv).start()
        self.start()

    def nameRequest(self):
        self.sock.send(pickle.dumps(["nameRequest",self.name]))
        sleep(1.5)

    def sendPasswd(self):
        passwd = getpass(self.data)
        self.sock.send(pickle.dumps(["passwd",passwd]))
        sleep(1.5)


    def auth(self):
        name = input(self.data)
        self.sock.send(pickle.dumps(["auth",name]))
        sleep(1.5)


    def success(self):
        print(self.data)
        self.status = "ready"

    '''
    Получение сообщений от сервера
    '''
    def recv(self):
        while True:
            try:
                self.data = self.sock.recv(1024)
                if not self.data: sys.exit(0)
                try:
                    status = pickle.loads(self.data)[0]
                    self.status = status
                    self.data = pickle.loads(self.data)[1]
                except:
                    print(self.data.decode())
            except OSError:
                break
    
    '''
    start
    '''
    def start(self):
        # while True:
        #     request = input('>')
        #     if request.lower() == "exit":
        #         self.sock.close()
        #         break
        #     elif request.lower().split()[0] == "scp":
        #         try:
        #             if request.lower().split()[1] == "-u":
        #                 with open(request.lower().split('/')[-1], "wb") as f:
        #                     while True:
        #                         data = conn.recv(1024)
        #                         if data == b"DONE":
        #                             break
        #                         f.write(data)
        #         except:
        #             file = os.path.realpath(request.split()[2])
        #             self.sock.send(pickle.dumps(["scp", request.split("/")[-1]]))
        #             sleep(0.3)
        #             with open(file, "rb") as f:
        #                 data = f.read(1024)
        #                 while data:
        #                     self.sock.send(data)
        #                     data = f.read(1024)
        #             self.sock.send(b"DONE")
        #     else:
        #         self.sock.send(pickle.dumps(request.split()))
         while self.status != 'finish':
            if self.status:
               if self.status == "auth":
                   self.auth()
               elif self.status == "passwd":
                   self.sendPasswd()
               elif self.status == "success":
                   self.success()
               elif self.status == "nameRequest":
                   self.nameRequest()
               else:
                   sleep(0.1)
                   request = input('>')
                   if request == "exit": 
                       self.status = "finish"
                       break
                   self.sock.send(pickle.dumps(request.split()))
Client()