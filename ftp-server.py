import socket
import os

'''
	pwd - current directory
	ls - list of files
	cat - file content
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
	req = req + ' _eoc_'
	if req.split(' ')[0] == 'pwd':																					#текущая директория
		return dirname
	
	elif req.split(' ')[0] == 'ls':																					#список файлов
		return '; '.join(os.listdir(dirname))
	
	elif req.split(' ')[0] == 'cat':																				#содержимое файла
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				with open(os.path.join(dirname,req.split(' ')[1]),'r') as f:
					return f.read()
			else:
				return 'no such file'
		else:
			return 'empty filename'
	
	elif req.split(' ')[0] == 'mkdir':
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				return 'dir (file) already exists!'
			else:
				os.mkdir(os.path.join(dirname,req.split(' ')[1]),777)
				return f'Dir is created!'
		else:
			return 'no filename'
	
	return 'bad request'																							#неправильный запрос


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(5)

while True:
	conn, addr = sock.accept()
	
	request = conn.recv(1024).decode()
	print(request)
	
	response = process(request)
	conn.send(response.encode())

	conn.close()
