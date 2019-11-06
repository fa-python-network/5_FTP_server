import socket
import os
from datetime import datetime
from threading import Thread
from functionFile import process
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

class FTPServer: 

	def __init__(self,log = "file.log"):
		self.log = log
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

	def listenToFTPClient(self,conn,addr):
		while True:
			request = conn.recv(1024).decode()
			if not request:
				conn.close()
				break
			response = process(request)
			conn.send(response.encode())
FTPServer()