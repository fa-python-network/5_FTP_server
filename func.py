import socket
import os
import ftplib
import time
from logger import Logfile
'''
pwd - показывает название рабочей директории
ls  - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
ls f - показывает содержимое 
mkdir <filename> - создание папки в текущей директории
rm <filename> - удалеяет папкy в текущей директории
delete <filename> - удаляет файл в текущей директории
rename <filename> <new name> - переименовывает файл/директорию в <new name>
exit - отключение клиента от сервера
copy.from <from> <filename> - копирует файл  с клиента (cl)/сервера (ser) (пример: copy.from cl f.txt)
'''

dirname = os.getcwd()

def process(r,conn):
	l=Logfile()
	req=r.split()
	if req[0] == 'pwd':
		return dirname

	elif req[0] == 'ls':
		return '; '.join(os.listdir(dirname))

	elif req[0] == 'ls f':
		pass

	elif req[0] == 'mkdir':
		try:
			path=str(os.getcwd())+'/'+req[1]
			#print(path)
		
			try:
				os.mkdir(path)
				p=path+' has been created'
				l.mkdir(req[1])
				return p
			except FileExistsError:
				return 'This path is already existed'
		except IndexError:
			return 'Вы не ввели название папки'

	elif req[0]== 'rm':
		try:
			try:
				path= os.path.abspath(req[1])
				os.rmdir(path,  dir_fd=None)
				l.rm(req[1])
				return 'The directory has been deleted'
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return 'Вы не ввели название папки'
	
	elif req[0] == 'delete':
		try:
			try:
				path= os.path.abspath(req[1])
				os.remove(path, dir_fd = None)
				l.delete(req[1])
				return 'The file has been deleted'
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return 'Вы не ввели название файла'
	
	elif req[0] == 'rename':
		try:
				try:
					path= os.path.abspath(req[1])
					try:
						 os.rename(req[1], req[2], src_dir_fd=None, dst_dir_fd=None)
						 l.rename(req[1],req[2])
						 return 'The name has been changed'
					except IndexError:
						return 'Вы не ввели новое название'
				except FileNotFoundError:
					return 'No such file or directory'


		except IndexError:
			return 'Вы не ввели название файла'
	
	elif req[0] == 'exit':
		l.serverend()
		return 'Disconnected'


	elif req[0] == 'copy.from':
		print("Tuta")
		if req[1] == 'cl':
			try:
				with open(req[2], "wb") as f:
					while True:
						data = conn.recv(1024)
						if data == b'sent':
							break
						f.write(data)
					return 'Файл отправлен'
				l.copyfromclienttoserver(req[2])
			except IndexError:
				return 'Вы не ввели название файла'

		elif req[1] == 'ser':
			try:
				file = os.path.realpath(req[2])
				time.sleep(0.3)
				with open(file, "rb") as f:
					data = f.read(1024)
					while data:
						conn.send(data)
						data = f.read(1024)
					time.sleep(3)
					conn.send(b'sent')
					return 'Файл принят'
				l.copyfromservertoclient(req[2])
			except IndexError:
				return 'Вы не ввели название файла'
		
		

	

	

	return 'Inappropriate request'