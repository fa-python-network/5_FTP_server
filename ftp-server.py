import socket
import os
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <directoryname> - создает директорию
rmdir <directoryname> - удаляет директорию
remove <filename> - удаляет путь к файлу
rename <filename> - переименовывает файл
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    
    rq = req.split()
    
    if req == 'pwd':
        return dirname
    
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    
    elif 'cat' in req:
    	with open(rq[1]) as file:
    		return file.read()
        
    elif 'mkdir' in req:    	
    	return os.mkdir(rq[1])
    
    elif 'rmdir' in req:
    	return shutil.rmtree(rq[1])
    
    elif 'remove' in req:
    	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), rq[1])
    	return os.remove(path)
    
    elif 'rename' in req:
    	return os.rename(rq[1], rq[2])
    
    else:
    	return 'Please, check the entered data and try again.'


PORT = 6666

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
    	conn.send('Your request is fulfilled'.encode())
    else:
    	conn.send(response.encode())

conn.close()
