import socket
import os
import hashlib
import pickle
import json
from datetime import datetime
from threading import Thread
from functionFile import process

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

class FTPServer:

    def __init__(self, log = "file.log", users = "users.json"):
        self.log = log
        self.users = users
        self.port = int(input("Введите порт: "))
        self.start()

    def start(self):
        self.sock = socket.socket()
        while True:
            try:
                self.sock.bind(('', self.port))
                break
            except:
                self.port+=1
        self.sock.listen(5)
        print(f'Установлен порт {self.port}')
        while True:
            conn, addr = self.sock.accept()
            self.serverStarted(addr)
            Thread(target = self.listenToFTPClient, args = (conn, addr)).start()

    def serverStarted(self, ip):
        with open(self.log, "a", encoding = "utf-8") as f:
            print(f'{datetime.now().time()} Server Launched {ip}', file = f)

    def serverStopped(self, ip):
        with open(self.log, "a", encoding = "utf-8") as f:
            print(f'{datetime.now().time()} Server Stopped {ip}', file = f)

    def checkPasswd(self, passwd, userkey) -> bool:
        key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
        return key == userkey

    def generateHash(self, passwd) -> bytes:
        key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
        return key

    def listenToFTPClient(self, conn, addr):
        client = self.authUser(conn)
        while True:
            request = conn.recv(1024)
            if not request:
                conn.close()
                break
            response = process(request, conn, client)
            conn.send(response.encode())

    def authUser(self, conn) -> str:
        try:
            open(self.users).close()
        except FileNotFoundError:
            open(self.users, 'a').close()
        with open(self.users, "r") as f:
            try:
                conn.send(pickle.dumps(["nameRequest", ""]))
                client = pickle.loads(conn.recv(1024))[1]
                users = json.load(f)
                try:
                    name = users[client]
                    conn.send(pickle.dumps(["passwd", "Введите свой пароль: "]))
                    passwd = pickle.loads(conn.recv(1024))[1]
                    conn.send(pickle.dumps(["success", f"Здравствуйте, {client}"])) if self.checkPasswd(passwd, name['password']) else self.checkUser(assr, conn)
                except: 
                    self.unknownUser(conn, users, client)
            except:
                self.unknownUser(conn, None, client, True)
        return client

    def unknownUser(self, conn, users, client, isJSONisNull = False):
        conn.send(pickle.dumps(["nameRequest", ""]))
        client = pickle.loads(conn.recv(1024))[1]
        conn.send(pickle.dumps(["passwd", "Неизвестный пользователь, введите свой пароль: "]))
        passwd = self.generateHash(pickle.loads(conn.recv(1024))[1])
        conn.send(pickle.dumps(["success", f"Здравствуйте, {client}"]))
        if isJSONisNull:
            with open(self.users, "w", encoding = "utf-8") as f:
                json.dump({client : {'password':passwd } }, f)
        else:
            users[client] = {'password':passwd}
            with open(self.users, "w", encoding = "utf-8") as f:
                json.dump(users, f)
        self.createUserDirectory(client)

    def createUserDirectory(self, name):
        process(pickle.dumps(["mkdir", f"{name}"]))

FTPServer()


