import os
import pickle
import socket
dirname = os.getcwd()

def process(data,conn):
	req=pickle.loads(data)
	if req[0] == 'pwd':
		return dirname

	elif req[0] == 'ls':
		return '; '.join(os.listdir(dirname))

	elif req[0] == 'ls f':
		pass

	elif req[0] == 'mkdir':
		try:
			path=str(os.getcwd())+'/'+req[1]
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
				path= os.path.abspath(req[1])
				os.rmdir(path,  dir_fd=None)
				return 'The directory has been deleted'
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return 'Wrong folder name'
	
	elif req[0] == 'delete':
		try:
			try:
				path= os.path.abspath(req[1])
				os.remove(path, dir_fd = None)
				return 'The file has been deleted'
			except FileNotFoundError:
				return 'No such file or directory'
			
		except IndexError:
			return "You don't wrote file name"
	
	elif req[0] == 'rename':
		try:
				try:
					path= os.path.abspath(req[1])
					try:
						 os.rename(req[1], req[2], src_dir_fd=None, dst_dir_fd=None)
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
		with open(req[1], "wb") as f:
			while True:
   				data = conn.recv(1024)
   				if data == b"DONE":
					   break
   				f.write(data)
		return "File sent"