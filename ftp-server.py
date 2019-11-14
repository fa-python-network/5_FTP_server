import socket
import os
import hashlib
import pickle
import json
from datetime import datetime
from threading import Thread
from functionFile import process
'''
Ограничьте возможности пользователя рамками одной определенной директории. Внутри нее он может делать все, что хочет: создавать и удалять любые файлы и папки. Нужно проследить, чтобы пользователь не мог совершить никаких действий вне пределов этой директории. Пользователь, в идеале, вообще не должен догадываться, что за пределами этой директории что-то есть.
Добавьте логирование всех действий сервера в файл. Можете использовать разные файлы для разных действий, например: подключения, авторизации, операции с файлами.
Добавьте возможность авторизации пользователя на сервере.
Добавьте возможность регистрации новых пользователей на сервере. При регистрации для пользователя создается новая рабочая папка (проще всего для ее имени использовать логин пользователя) и сфера деятельности этого пользователя ограничивается этой папкой.
Реализуете квотирование дискового пространства для каждого пользователя.
Реализуйте учётную запись администратора сервера.
Напишите отладочный клиент. Клиент должен подключаться к серверу и в автоматическом режиме тестировать корректность его работы. Используйте подход, аналогичный написанию модульных тестов. Клиент должен вывести предупреждающее сообщение, если сервер работает некорректно.
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

class FTPServer: 

	def __init__(self, log = "file.log", users = "users.json"):
		self.log = log
		self.users = users
		self.port = int(input("Введите порт:"))
		self.start()

	def start(self):
		self.sock = socket.socket()
		while True:	
 			try:	
 				self.sock.bind(('',self.port))
 				break
 			except:
 				self.port+=1		
		self.sock.listen(5)
		print(f'Установлен порт {self.port}')
		while True:
			conn, addr = self.sock.accept()
			self.serverStarted(addr)
			Thread(target = self.listenToFTPClient,args = (conn,addr)).start()

	def serverStarted(self,ip):
		with open(self.log, "a", encoding="utf-8") as f:
			print(f'{datetime.now().time()} Server Launched {ip}', file=f)

	def serverStopped(self,ip):
		with open(self.log, "a", encoding="utf-8") as f:
			print(f'{datetime.now().time()} Server Stopped {ip}', file = f)

	def checkPasswrd(self, passwd, userkey) -> bool:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key == userkey

	def generateHash(self, passwd) -> bytes:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key
	'''
	Прослушка пользователя
	'''
	def listenToFTPClient(self,conn,addr):
		client = self.authUser(conn)
		while True:
			request = conn.recv(1024)
			if not request:
				conn.close()
				break
			
			response = process(request,conn,client)
			conn.send(response.encode())

	'''
	Авторизация пользователя
	'''		
	def authUser(self, conn) -> str:
		try:
			open(self.users).close()
		except FileNotFoundError:
			open(self.users, 'a').close()
		with open(self.users, "r") as f:
			try:
				conn.send(pickle.dumps(["nameRequest",""]))
				client = pickle.loads(conn.recv(1024))[1]
				users = json.load(f)
				try:
					name = users[client]
					conn.send(pickle.dumps(["passwd","Введите свой пароль: "]))
					passwd = pickle.loads(conn.recv(1024))[1]
					conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"])) if self.checkPasswrd(passwd,name['password']) else self.checkUser(addr,conn)
				except: self.unknownUser(conn,users,client)
			except:
				self.unknownUser(conn, None, client, True)
		return client
					
	def unknownUser(self,conn, users, client, isJSONisNill = False):
		conn.send(pickle.dumps(["nameRequest",""]))
		client = pickle.loads(conn.recv(1024))[1]
		conn.send(pickle.dumps(["passwd","Я тебя не знаю, введите свой пароль: "]))
		passwd = self.generateHash(pickle.loads(conn.recv(1024))[1])
		conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
		if isJSONisNill:
			with open(self.users, "w", encoding="utf-8") as f:
					json.dump({client : {'password': passwd} },f)
		else:
			users[client] = {'password': passwd}
			with open(self.users, "w", encoding="utf-8") as f:
				json.dump(users,f)
		self.createUserDirectory(client)

	def createUserDirectory(self, name):
		process(pickle.dumps(["mkdir", f"{name}"]))
FTPServer()