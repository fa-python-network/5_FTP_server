import socket
import os

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
exit - отключение клиента
mkdir <directory name> - создание директории
rmdir <directory name> - удаление директории и всего содержимого рекурсивно
rm <filename> - удаление файла
rename <filename> <new filename> - переименование файла
cts <filename> - копирование файла на сервер
ctc <filename> - копирование файла на клиент
'''

PORT = 1260
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


def rename(req):
    try:
        src = req[:req.find(' ')]
        dst = req[req.find(' ')+1:]
        os.rename(src, dst)
        return ''
    except OSError:
        return "No such file or directory"
    except:
        return "Ivalid value"


def cts(filename):
    a = b''
    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            break
        a += data
    with open(filename, 'wb') as f:
        f.write(a)
    return ''


def ctc(req):
    return ''


def process(req):
    if req == 'exit':
        return 'exit'
    elif req == 'pwd':
        return curr_dir
    elif req == 'ls':
        return '\n'.join(os.listdir(curr_dir))
    elif req[:4] == 'cat ':
        return cat(req)
    elif req[:6] == 'mkdir ':
        return mkdir(req)
    elif req[:6] == 'rmdir ':
        return rmdir(req[6:])
    elif req[:3] == 'rm ':
        return rm(req[3:])
    elif req[:7] == 'rename ':
        return rename(req[7:])
    elif req[:4] == 'cts ':
        return cts(req[4:])
    elif req[:4] == 'ctc ':
        return cts(req[4:])
    else:
        return 'bad request'


sock = socket.socket()
sock.bind(('', PORT))

sock.listen(0)
while True:
    print("Слушаем порт")
    conn, addr = sock.accept()
    conn.settimeout(1)

    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())
    conn.close()
    if request == 'exit':
        print("Client otrubil server nafig")
        sock.close()
        break

