import socket
import os
import shutil

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <Название папки> - создает новую папку
rmdir <Название папки> - удаляет папку
create <Название файла> - создает файл
remove <Название файла> - удаляет файл
rename <Название файла> - переименовывает файл
copy <Название файла> <Название нового файла> - копирует файл
'''

dirname = os.path.join(os.getcwd(), 'docs')
def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req[:3] == 'cat':
        path = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.exists(path):
            with open(path, 'r+') as f:
                line = ''
                for l in f:
                    line+=l
            return line
        else:
            return 'Такого файла не существет'
    elif req[:5] == 'mkdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if not os.path.exists(path):
            os.makedirs(path)
            return f'Папка создана'
        else: 
            return 'Такая папка уже существет'
    elif req[:5] == 'rmdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if os.path.exists(path):
            shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6::]))
            return f'Папка удалена'
        else:
            return 'Такой папки не существует'
    elif req[:6]  == 'create':
        open(os.path.join(os.getcwd(), 'docs', req[7:]), 'tw', encoding='utf-8').close()
        return f'Файл создан'
    elif req[:6]  == 'remove':
        os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
        return f'Файл удален'
    elif req[:6]  == 'rename':
        req = req.split(' ')
        os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл переименован'
    elif req[:4]  == 'copy':
        req = req.split(' ')
        shutil.copyfile(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл скопирован'
    return 'bad request'

PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт: ", PORT)
while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())
conn.close()
