import socket
import os
import shutil

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
P.S. Остальные команды прописаны в комментариях, тут делать список лень :)
'''

dirname = os.path.join(os.getcwd(), 'docs')


def process(req):
    # Где мы находимся(путь)
    if req == 'pwd':
        return dirname

    # Просматриваем файлы и папки
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))

    # Просматриваем файл
    elif req[:3] == 'cat':
        path = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.exists(path):
            with open(path, 'r+') as file:
                line = ''
                for l in file:
                    line += l
            return line
        else:
            return 'Файла не существует'

    # Создаем папку
    elif req[:5] == 'mkdir':
        path = os.path.join(os.getcwd(), 'docs', req[6:])
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return f'Папка {req[6:]} создана!'
        else:
            return f'Неверный ввод {req[6:]}'


    # Рекурсивное удаление пустой папки
    elif req[:5] == 'rmdir':
        if req[5] == " ":
            path = os.path.join(os.getcwd(), 'docs', req[6:])
            if os.path.exists(path):
                os.rmdir(path)
                return f'Папка {req[6:]} удалена'
            else:
                return f'Папки {req[6:]} не существует'
        else:
            return f'Команда введена неверно!'


    # Создание файла
    elif req[:6] == 'create':
        path = os.path.join(os.getcwd(), 'docs', req[7:])
        open(path, 'tw', encoding='utf-8')
        return f'Файл {req[7:]} был создан!'



    # Удаление файла
    elif req[:6] == 'remove':
        path = os.path.join(os.getcwd(), 'docs', req[7:])
        try:
            os.remove(path)
            return f'Файл {req[7:]} был удален!'

        except:
            return f'Файл не был найден'


    # Переименуем файл
    elif req[:6] == 'rename':
        if req[6] == " ":
            try:
                req_s = req.split(' ')
                path1 = os.path.join(os.getcwd(), 'docs', req_s[1])
                path2 = os.path.join(os.getcwd(), 'docs', req_s[2])
                os.rename(path1, path2)
                return f'Файл {req_s[1]} был переименован в {req_s[2]}'

            except:
                return f'Не в этот раз'



    # Копирование файла
    elif req[:4] == 'copy':
        if req[4] == " ":
            try:
                req_s = req.split(' ')
                path1 = os.path.join(os.getcwd(), 'docs', req_s[1])
                path2 = os.path.join(os.getcwd(), 'docs', req_s[2])
                shutil.copyfile(path1, path2, follow_symlinks=True)
                return f'Файл {req_s[1]} скопирован!'

            except:
                f'Копирование прошло неудачно, попробуйте ввести корректное имя файла!'

    return 'bad request'


PORT = 6670

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


