import socket
import os

'''
	pwd - current directory
	ls - list of files
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
	if req == 'pwd':
		return dirname
	elif req == 'ls':
		return '; '.join(os.listdir(dirname))
	return 'bad request'


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
