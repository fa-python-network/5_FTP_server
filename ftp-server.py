import socket
import os
import shutil



directory = os.path.join(os.getcwd(), 'docs')
def process(req):

    if req == 'pwd':
        return directory

    elif req == 'ls':
        return '; '.join(os.listdir(directory))

    elif req[:3] == 'cat':
        path = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.exists(path):
                with open(path, 'r+') as file:
                    line = ''
                    for l in file:
                        line+=l
                return line
        else:'Операция не выполнена'
            
    elif req[:5] == 'mkdir':
        path = os.path.join(os.getcwd(), 'docs', req[6:])
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return 'Операция выполнена успешно'

    elif req[:5] == 'rmdir':
        if req == " ":
            path = os.path.join(os.getcwd(), 'docs', req[6:])
            if os.path.exists(path):
                os.rmdir(path)
                return 'Операция выполнена успешно'

    elif reqreq[:5] == 'touch':
        path = os.path.join(os.getcwd(), 'docs', req[6:])
        open(path,'tw')
        return 'Операция выполнена успешно'


    elif reqreq[:6] == 'remove':
        path = os.path.join(os.getcwd(), 'docs', req[7:])
        try:
            os.remove(path)
            return 'Операция выполнена успешно'
        except:
            return 'Операция не выполнена'

    elif reqreq[:6] == 'rename':
        if req[:6] == " ":
            try:
                req_s = req.split(' ')
                path1 = os.path.join(os.getcwd(), 'docs', req_s[1])
                path2 = os.path.join(os.getcwd(), 'docs',req_s[2])
                os.rename(path1, path2)
                return 'Операция выполнена успешно'
            except:
                return 'Операция не выполнена'
    elif req[:4]  == 'copy':
        if req[:4] == " ":
            try:
                req_s = req.split(' ')
                path1 = os.path.join(os.getcwd(), 'docs', req_s[1])
                path2 = os.path.join(os.getcwd(), 'docs', req_s[2])
                shutil.copyfile(path1, path2, follow_symlinks=True)
                return 'Операция выполнена успешно'
            except:
                'Операция не выполнена'
    return 'bad request'


PORT = 9090

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

print("Порт:", PORT)

while True:

    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())

conn.close()