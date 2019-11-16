import socket
import os
from logger import Logfile
from func import process
from datetime import datetime
from threading import Thread
from time import sleep
import os
import hashlib
import json
import pickle
import sys


'''
процедуры для сервера
'''
def createUserDirectory(name):
	
	path=str(os.getcwd())+'/'+name
	#print(path)
	os.mkdir(path)
	os.chdir(path)
	

def listenToClient(conn, address):
	print('Слушаю клиента')
	authUser(address,conn)
	while True:
				data = conn.recv(1024)
				if data:
					try:
						status, data = pickle.loads(data)
						if status == "finish":
							
							conn.send(pickle.dumps(["finish", ""]))
							#conn.close()
					except:
						
						status = process(data.decode(),conn)
						conn.send(status.encode())
					
				else:
					conn.close()
					break


def authUser(addr,conn):
		
		try:
			open("users.json").close()
		except FileNotFoundError:
			open("users.json", 'a').close()
		with open("users.json", "r") as f:
			try:
				conn.send(pickle.dumps(["nameRequest",""]))
				client = pickle.loads(conn.recv(1024))[1]
				users = json.load(f)
				try:
					name = users[client]
					conn.send(pickle.dumps(["passwd","Введите свой пароль: "]))
					passwd = pickle.loads(conn.recv(1024))[1]
					if checkPasswrd(passwd,name['password']):
						conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
						path=str(os.getcwd())+'/'+client
						
						os.chdir(path)
						print(os.getcwd())
					else:
						authUser(addr,conn)

					#conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"])) if checkPasswrd(passwd,name['password']) else authUser(addr,conn)
					
					
					
				except: 
					
					unknownUser(conn,users,client, "newUSER")
			except:
				
				unknownUser(conn,None,client, "newJSON")
def unknownUser(conn, users, client, key):
	
	conn.send(pickle.dumps(["passwd","Я тебя не знаю, ведите свой пароль: "]))
	passwd = generateHash(pickle.loads(conn.recv(1024))[1])
	conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
	if key == "newJSON":
		with open("users.json", "w", encoding="utf-8") as f:
			json.dump({client : {'password': passwd} },f)
	else:
		users[client] = {'password': passwd}
		with open("users.json", "w", encoding="utf-8") as f:
			json.dump(users,f)	
	createUserDirectory(client)
			


def checkPasswrd( passwd, userkey) -> bool:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key == userkey

def generateHash( passwd) -> bytes:
		key = hashlib.md5(passwd.encode() + b'salt').hexdigest()
		return key

def newUser(conn, users):
		conn.send(pickle.dumps(["nameRequest",""]))
		client = pickle.loads(conn.recv(1024))[1]
		conn.send(pickle.dumps(["passwd","Я вас еще не знаю, поэтому придумайте себе пароль : "]))
		passwd = generateHash(pickle.loads(conn.recv(1024))[1])
		conn.send(pickle.dumps(["success",f"Здравствуйте, {client}"]))
		users[client] = {'password': passwd}
		
		with open("users.json", "w", encoding="utf-8") as f:
			json.dump(users,f)

'''
дальше запуск сервера
'''



try:
    port=int(input("ваш порт:"))
    if not 0 <= port <= 65535:
        raise ValueError
except ValueError :
    port = 9090


sock = socket.socket()
sock.bind(('', port))
sock.listen()
print("Прослушиваем порт:", port)


conn, addr = sock.accept()
listenToClient(conn,addr)
conn.close()





