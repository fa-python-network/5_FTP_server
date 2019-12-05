import socket
import os
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <dirname>- создает директорию
rmdir <dirname>-удаляет директорию
mkf <filename>-создает файл
remove <filename> - удаляет файла
rename <filename>- переименовывает файл
'''

directory = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return directory
    elif req == 'ls':
        return '; '.join(os.listdir(directory))
    elif 'cat'in req:
        name=req.split()[1]
        f=open(os.path.join(os.path.abspath(os.path.directory(__file__)), directory+"/"+name))
        return f.read()
    elif 'mkdir' in req:
        name=req.split()[1]
        return os.mkdir(directory+"/"+name)
    elif 'rmdir' in req:
        name=req.split()[1]
        return shutil.rmtree(directory+"/"+name)
    elif 'mkf' in req:
        name=req.split()[1]
        new = './docs/new_f.txt'
        new_f = open(new, mode='w', encoding='latin_1')
        new_f.close()            
        return os.rename(directory+"/new_f.txt",directory+"/"+name)
    elif 'remove' in req:
        name=req.split()[1]
        path = os.path.join(os.path.abspath(os.path.directory(__file__)), directory+"/"+name)
        return os.remove(path)
    elif 'rename' in req:
        old=req.split()[1]
        new=req.split()[2]
        return os.rename(directory+"/"+old,directory+"/"+new)
    return 'Bad request.'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

while True:
    print("Порт: ", PORT)
    conn, addr = sock.accept()
    print(addr)
    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    if (request == 'pwd') or (request == 'ls') or ('cat' in request):
        conn.send(response.encode())
    elif ('mkdir' in request):
        conn.send('Директория "{}" создана'.format(request.split()[1]).encode())
    elif ('rmdir' in request):
        conn.send('Директория "{}" удалена'.format(request.split()[1]).encode())
    elif ('remove' in request):
        conn.send('Файл "{}" удален'.format(request.split()[1]).encode())
    elif ('rename' in request):
        conn.send('Файл "{}" переименован в {}'.format(request.split()[1],request.split()[2]).encode())
    elif ('mkf' in request):
        conn.send('Файл "{}" создан'.format(request.split()[1]).encode())
    else:
        conn.send(response.encode())

conn.close()
