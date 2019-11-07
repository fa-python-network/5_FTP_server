import socket
import os
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif 'cat' in req:
    	file = req.split()
    	with open(file[1],"r") as f:
    		return f.read()
    elif 'mkdir' in req:
    	directory = req.split()
    	return os.mkdir(directory[1])
    elif 'rmdir' in req:
    	directory = req.split()
    	return shutil.rmtree(directory[1])
    elif 'remove' in req:
    	file = req.split()
    	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file[1])
    	return os.remove(path)
    elif 'rename' in req:
    	file = req.split()
    	return os.rename(file[1], file[2])
    else:
    	return 'Something wrong...'


PORT = 6680

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    if (request=='pwd') or (request=='ls') or ('cat' in request):
    	conn.send(response.encode())
    elif ('mkdir' in request) or ('rmdir' in request) or ('remove' in request) or ('rename' in request):
    	conn.send('Complete.'.encode())
    else:
    	conn.send(response.encode())

conn.close()
