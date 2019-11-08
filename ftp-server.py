import socket
import os
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    req_list = req.split()
    if req_list[0] == 'pwd':
        return dirname
    elif req_list[0] == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req_list[0] == "mkdir":
        if len(req_list) < 2 or req_list[1] == "":
            return 'bad request'
        try:
            new_path = os.path.join(dirname, req_list[1])
            os.mkdir(new_path)
            return 'added'
        except:
            return 'folder exists'

    elif req_list[0] == "remove":
        if len(req_list) < 2 or req_list[1] == "":
            return 'bad request'
        try:
            new_path = os.path.join(dirname, req_list[1])
            os.remove(new_path)
            return 'removed'
        except:
            return 'error'

    elif req_list[0] == "rmdir":
        if len(req_list) < 2 or req_list[1] == "":
            return 'bad request'
        try:
            new_path = os.path.join(dirname, req_list[1])
            os.rmdir(new_path)
            return 'removed'
        except:
            return 'error'

    elif req_list[0] == "rename":
        if len(req_list) < 3 or req_list[1] == "" or req_list[2] == "":
            return 'bad request'
        try:
            old_path = os.path.join(dirname, req_list[1])
            new_path = os.path.join(dirname, req_list[2])
            os.rename(old_path, new_path)
            return 'renamed'
        except:
            return 'error'
    elif req_list[0] == "CtS":
        new_path = os.path.join(dirname, req_list[1])
        conn.send("OK".encode())
        f = open(new_path, 'wb')
        hash = conn.recv(1024)
        while hash:
            f.write(hash)
            hash = conn.recv(1024)
            if (hash.decode() == 'END'):
                break
        f.close()
        return 'added'

    return 'bad request'


PORT = 6662

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
