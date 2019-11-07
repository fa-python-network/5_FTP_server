import socket
import os
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <dir> - создаёт папку
'''

userdir = os.path.join(os.getcwd(), 'docs')

def check_access(dir):
    pass

def pwd():
    return userdir

def ls(dir):
    return '; '.join(os.listdir(dir))

def cat(dir):
    content=str()
    with open(dir,'r') as f:
        for line in f:
            content+=line
    return content
    
def mkdir(dir):
    if not os.path.exists(os.path.join(os.getcwd(),'docs',dir)):
        os.mkdir(dir)
    return ''

def process(req):
    if req == 'pwd':
        pwd()
    elif req == 'ls':
        ls(userdir)
    elif req.split()[0]=='cat':
        cat(req.split()[1])
    elif req.split()[0]=='mkdir':
        mkdir(req.split()[1])
    else:
        return 'bad request'


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
    conn.send(response.encode())

    conn.close()
