import socket
import os
import shutil

"""
pwd - показывает назване рабочей папки
cut - показывает содержимое файла
ls - показывает одержимое рабочей папки
cat <filename> - показывает содержимое файла
mkdir <dirname> - создать новую директорию")
rmdir <dirname> - удалить пустую директорию")
create <filename> <text> - создать файл, записать в него текст <text>")
remove <filename> - удалить файл")
rename <filename> <newfilename> - переименовать файл
"""

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
                str = ''
                for l in f:
                    str += l
            return str
        else:
            return 'Такого файла не существет'


    elif req[:5] == 'mkdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if not os.path.exists(path):
            os.makedirs(path)
            return f'Папка {req[:5]} создана'


    elif req[:5] == 'rmdir':
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if os.path.exists(path):
            shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6::]))
            return f'Папка {req[6::]} удалена'
        else:
            return 'Такой папки не существует'


    elif req[:6] == 'create':
        open(os.path.join(os.getcwd(), 'docs', req[7:]), 'tw', encoding='utf-8').close()
        return f'Файл {req[8:]} создан'


    elif req[:6] == 'remove':
        os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
        return f'Файл {req[7:]} удален'


    elif req[:6]  == 'rename':
        req = req.split(' ')
        os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл переименован'


    elif req[:14] == 'copy_to_server':
        file1 = os.path.join(os.getcwd(), 'docs', req.split()[2])
        file2 = os.path.join(dirname, req.split()[1])
        shutil.copyfile(file1, file2)
        return 'Успешное копирование'

    elif req[:16] == 'copy_from_server':
        file1 = os.path.join(os.getcwd(), 'docs', req.split()[2])
        file2 = os.path.join(dirname, req.split()[1])
        shutil.copyfile(file2, file1)
        return 'Успешное копирование'

    else:
        return 'bad request'


PORT = 9090
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