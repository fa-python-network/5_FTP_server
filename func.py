import socket
import os
import ftplib
import time
from logger import Logfile
'''

ls  - показывает содержимое текущей директории
mkdir <filename> - создание папки в текущей директории
rm <filename> - удалеяет папкy в текущей директории
delete <filename> - удаляет файл в текущей директории
rename <filename> <new name> - переименовывает файл/директорию в <new name>
exit - отключение клиента от сервера
copy.from <from> <filename> - копирует файл  с клиента (cl)/сервера (ser) (пример: copy.from cl f.txt)
'''

dirname = os.getcwd()

def process(r,conn):
	#print(os.getcwd())
	log=Logfile()
	# for i in r:
	# 	if i=='/':
	# 		return('Название файла указывается без абсолютного пути')
	req=r.split()
	
        
	
	

	if req[0] == 'ls':
		return '; '.join(os.listdir(dirname))

	

	elif req[0] == 'mkdir':
		try:
			path=str(os.getcwd())+'/'+req[1]
			#print(path)
		
			try:
				th = os.getcwd()
				t=th.split('/')[-1]
				re = os.path.realpath(r.split()[1])
				re=re.split('/')[-2]
				if re != t:
					return('Отказано в доступе')
				os.mkdir(path)
				p=req[1]+' has been created'
				log.mkdir(req[1])
				return p
			except FileExistsError:
				return 'This path is already existed'
		except IndexError:
			return 'Вы не ввели название папки'

	elif req[0]== 'rm':
		try:
			try:
				path= os.path.abspath(req[1])
				th = os.getcwd()
				t=th.split('/')[-1]
				re = os.path.realpath(r.split()[1])
				re=re.split('/')[-2]
				if re == t:
					os.rmdir(path,  dir_fd=None)
					log.rm(req[1])
					return 'The directory has been deleted'
				return('Отказано в доступе')
				
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return 'Вы не ввели название папки'
	
	elif req[0] == 'delete':
		try:
			try:
				path= os.path.abspath(req[1])
				th = os.getcwd()
				t=th.split('/')[-1]
				re = os.path.realpath(r.split()[1])
				re=re.split('/')[-2]
				if re == t :
					os.remove(path, dir_fd = None)
					log.delete(req[1])
					return 'The file has been deleted'
				return('Отказано в доступе')
				
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
						 
						 log.rename(req[1],req[2])
						 return 'The name has been changed'
					except IndexError:
						return 'Вы не ввели новое название'
				except :
					return 'No such file or directory'


		except IndexError:
			return 'Вы не ввели название файла'
	
	elif req[0] == 'exit':
		
		
		return 'Disconnected'


	elif req[0] == 'copy.from':
		if req[1] == 'cl':
			try:
				with open(req[2], "wb") as f:
					while True:
						data = conn.recv(1024)
						if data == b'sent':
							break
						f.write(data)
					log.copyfromclienttoserver(req[2])
					return 'Файл отправлен'
				
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
					log.copyfromservertoclient(req[2])
					return 'Файл принят'
				
			except IndexError:
				return 'Вы не ввели название файла'
		
		

	

	

	return 'Inappropriate request'