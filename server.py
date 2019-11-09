import socket
import os

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

PORT = 1253
os.chdir('docs')
curr_dir = os.getcwd()


def cat(req):
    filename = req[4:]
    try:
        filename = curr_dir + '/' + filename
        with open(filename) as f:
            return f.read()
    except OSError:
        return "NET TAKOGO FAILA!!!!!!!!!"

def mkdir(req):
    dirname = req[6:]
    try:
        dirname = curr_dir + '/' + dirname
        os.mkdir(dirname)
        return ''
    except OSError:
        return "This directory already exists"

def rmdir(req):
    try:
        os.rmdir(curr_dir+'/'+req)
        return ''
    except:
        os.chdir(curr_dir+'/'+req)
        for i in os.listdir(curr_dir+'/'+req):
            try:
                rmdir(req+'/'+i)
            except:
                os.remove(i)
        os.chdir(curr_dir+'/..')
        os.rmdir(curr_dir+'/'+req)
        return ''

def rm(req):
    filename = req
    try:
        os.remove(curr_dir+'/'+filename)
        return ''
    except OSError:
        return "This file does not exist"

def process(req):
    if req == 'exit':
        return 'exit'
    elif req == 'pwd':
        return curr_dir
    elif req == 'ls':
        return '; '.join(os.listdir(curr_dir))
    elif req[:4] == 'cat ':
        return cat(req)
    elif req[:6] == 'mkdir ':
        return mkdir(req)
    elif req[:6] == 'rmdir ':
        return rmdir(req[6:])
    elif req[:3] == 'rm ':
        return rm(req[3:])
    else:
        return 'bad request'


sock = socket.socket()
sock.bind(('', PORT))

sock.listen(0)
while True:
    print("Слушаем порт")
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())
    conn.close()
    if request == 'exit':
        print("Client otrubil server nafig")
        sock.close()
        break

