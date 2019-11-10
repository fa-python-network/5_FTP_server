import socket
import os
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

    elif req.strip()[:5] == 'mkdir':
        new_dir = os.path.join(dirname, req.strip()[6:])
        if os.path.isdir(new_dir) == False:
            os.mkdir(new_dir)
            return 'dir is created'
        else:
            return 'you cant create what has been created already'

    elif req.strip()[:5] == 'rmdir':
        del_dir = os.path.join(dirname, req.strip()[6:])
        if os.path.isdir(del_dir) == False:
            return 'you cant delete what does not exist, silly'
        else:
            os.rmdir(del_dir)
            return str(del_dir) + ' is removed, my lord'

    elif req.strip()[:6] == 'rename':
        old_name = os.path.join(dirname, req.split(' ')[1])
        new_name = os.path.join(dirname, req.split(' ')[2])
        if os.path.isdir(os.path.join(dirname,old_name)) == True:
            os.rename(old_name, new_name)
            return 'it is renamed'
        else:
            return 'there is no such directory ' + str(old_name)

    elif req.strip()[:6] == 'rmfile':
        del_file = os.path.join(dirname, req.strip()[7:])
        if os.path.isfile(del_file) == True:
            os.remove(del_file)
            return str(del_file) + ' is removed'
        else:
            return 'there is no such file'

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

'''
    elif req.strip()[:2] == 'cd':
        destination = os.path.join(dirname, req.strip()[3:])
        print(destination)
        if os.path.isdir(destination) == True:
            os.chdir(destination)
            return os.getcwd()
        else:
            return 'there is no such directory ' + str(destination)
'''

