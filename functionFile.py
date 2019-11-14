import os
import pickle
import socket
import time
def process(data,conn = None, client = None):
	req=pickle.loads(data)
	dirname = f"{os.getcwd()}/{client}"
	if req[0] == 'pwd':
		return dirname

	elif req[0] == 'ls':
		return '; '.join(os.listdir(dirname))

	elif req[0] == 'ls f':
		pass

	elif req[0] == 'mkdir':
		try:
			path=dirname+'/'+req[1]
			try:
				os.mkdir(path)
				p=path+' has been created'
				return p
			except FileExistsError:
				return 'This path is already existed'
		except IndexError:
			return 'Wrong folder name'

	elif req[0]== 'rm':
		try:
			try:
				os.rmdir(dirname+'/'+req[1],  dir_fd=None)
				return 'The directory has been deleted'
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return 'Wrong folder name'
	
	elif req[0] == 'delete':
		try:
			try:
				os.remove(dirname+'/'+req[1], dir_fd = None)
				return 'The file has been deleted'
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return "You don't wrote file name"
	
	elif req[0] == 'rename':
		try:
				try:
					try:
						 os.rename(dirname+'/'+req[1], req[2], src_dir_fd=None, dst_dir_fd=None)
						 return 'The name has been changed'
					except IndexError:
						return "You don't wrote ma,e"
				except FileNotFoundError:
					return 'No such file or directory'


		except IndexError:
			return "You don't wrote file name"
	
	elif req[0] == 'exit':
		return 'Disconnected'
	elif req[0] == "scp":
		if req[2] == "-u":
				file = os.path.realpath(req[1])
				time.sleep(0.3)
				with open(file, "rb") as f:
					data = f.read(1024)
					print("Here")
					while data:
						conn.send(data)
						data = f.read(1024)
				conn.send(b"DONE")
				return "File recieved"
		else:
			with open(client+'/'+req[2], "wb") as f:
				while True:
					data = conn.recv(1024)
					print(data)
					if data == b"DONE":
						print("Finish")
						break
					f.write(data)
			return "File sent"