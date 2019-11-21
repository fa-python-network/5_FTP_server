import socket
import os
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <dirname> - создать новую директорию
rmdir <dirname> - удалить пустую директорию
create <filename> <text> - создать файл, записать в него текст <text>
remove <filename> - удалить файл
rename <oldfilename> <newfilename> - переименовать файл
copy_to_server <filename1> <filename2> -  отправить файл с клиента на сервер
copy_from_server <filename1> <filename2> - скачать файл с сервера на клиент
exit - выход
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):

    if req == 'pwd':
        return dirname

    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    
    elif req[:3] == 'cat':
        if req[3] == ' ':
            path = os.path.join(os.getcwd(), 'docs', req[4:])
            if os.path.exists(path):
                with open(path, 'r') as f:
                    str_ = ''
                    for i in f:
                        str_+=i
                    if str_ =="":
                        conn.send('Файл пуст'.encode())
                return str_
            else:
                return f'Файла {req[4:]}\nне существует в данной директории'
        else:
            return 'Неправильный ввод команды cat'


    elif req[:5] == 'mkdir':
        if req[5] == " ":
            path = os.path.join(os.getcwd(), 'docs', req[6:])
            if not os.path.exists(path):
                os.makedirs(path)
                return f'Папка {req[6:]} создана'
            else: 
                return f'Неправильный ввод либо папка {req[6:]}\nуже существет, придумайте другое имя для папки'
        else:
            return 'Неправильный ввод команды mkdir'

    elif req[:5] == 'rmdir':
        if req[5] == " ":
            path = os.path.join(os.getcwd(), 'docs', req[6:])
            if os.path.exists(path):
                shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6:]))
                return f'Папка {req[6:]} удалена'
            else:
                return f'Папки {req[6:]}не существует'
        else:
            return 'Неправильный ввод команды rmdir'

    elif req[:6]  == 'create':
        if req[6] == " ":
            req = req.split(' ')
            file_text = ' '.join(req[2:])
            with open(os.path.join(os.getcwd(), 'docs', req[1]), 'tw', encoding='utf-8') as f:
                f.write(file_text)
            return f'Файл создан'
        else:
            return 'Неправильный ввод команды create'

    elif req[:6]  == 'remove':
        os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
        return f'Файл {req[7:]} удален'

    elif req[:6]  == 'rename':
        if req[6] == " ":
            req = req.split(' ')
            os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
            return 'Файл переименован'
        else:
            return 'Неправильный ввод команды remove'

    elif req[:14] == 'copy_to_server':
        if req[14] == " ":
            file1 = os.path.join(os.getcwd(), 'docs', req.split()[2])
            file2 = os.path.join(dirname, req.split()[1])
            shutil.copyfile(file1, file2)
            return 'Успешное копирование'
        else:
            return 'Неправильный ввод команды copy_to_server'

    elif req[:16] == 'copy_from_server':
        if req[16] == " ":
            file1 = os.path.join(os.getcwd(), 'docs', req.split()[2])
            file2 = os.path.join(dirname, req.split()[1])
            shutil.copyfile(file2, file1)
            return 'Успешное копирование'
        else:
            return 'Неправильный ввод команды copy_from_server'

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
