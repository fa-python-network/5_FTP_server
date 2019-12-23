import socket
import threading
import logging
import os
import shutil

sock = socket.socket()
logging.basicConfig(filename = "exp.log", filemode = "w", level = logging.INFO)

client_host_port = 1024
while client_host_port != 65536:
    try:
        logging.info(f'Сервер пытается подключиться к порту: {client_host_port}')
        sock.bind(('', client_host_port))
        break
    except:
        logging.error(f'При подключении к порту {client_host_port} возникла ошибка')
        client_host_port += 1

sock.listen(100)

print('Порт: ', client_host_port)
logging.info(f'Подключено к порту: {client_host_port}\n')

def lazy_output(addr, data):
    print(f"Пользователь {addr} закончил сессию")
    print("Пользовательский ввод:", data, f"Пользователь: {addr}")
    logging.info(f"Пользователь {addr} заканчивает сессию\n")

def process(req):

    dirname = os.path.join(os.getcwd(), 'docs')
    if req.strip() == 'pwd':
        logging.info(dirname)
        return dirname

    elif req.strip() == 'ls':
        logging.info('; '.join(os.listdir(dirname)))
        return '; '.join(os.listdir(dirname))

    elif req.strip()[:6] == 'mkfile':
        user_new_file = os.path.join(dirname, req.strip()[7:])
        if os.path.isfile(user_new_file) == True:
            return "Файл уже существует"
        else:
            file = open(user_new_file, 'w')
            file.close()
            return "Файл успешно создан!"

    elif req.strip()[:6] == 'remove':
        user_file = os.path.join(dirname, req.strip()[7:])
        if os.path.isfile(user_file) == True:
            os.remove(user_file)
            return "Файл успешно удалён"
        else:
            return "Файл не существует в текущей директории"

    elif req.strip()[:5] == 'mkdir':
        user_new_dir = os.path.join(dirname, req.strip()[6:])
        if os.path.isdir(user_new_dir) == True:
            return "Такая папка уже существует"
        else:
            os.mkdir(user_new_dir)
            return "Папка успешно создана!"

    elif req.strip()[:5] == 'rmdir':
        user_dir = os.path.join(dirname, req.strip()[6:])
        if os.path.isdir(user_dir) == True:
            os.rmdir(user_dir)
            return "Папка успешно удалена"
        else:
            return "Папка не существует"

    elif req.strip()[:6] == 'rmtree':
        user_dir = os.path.join(dirname, req.strip()[7:])
        if os.path.isdir(user_dir) == True:
            shutil.rmtree(user_dir)
            return "Папка успешно удалена"
        else:
            return "Папка не существует"

   
    logging.info('Неправильный запрос\n')
    return 'bad request'

def user_input(conn, addr):
    msg = ''
    while True:
        data = conn.recv(1024).decode()
        logging.info(f"Пользовательский ввод: {data}. Пользователь: {addr}")
        if not data:
            lazy_output(addr, msg)
            break
        try:
            response = process(data)
            if response == 'bad request':
                msg += data + ' '
            conn.send(response.encode())
        except:
            pass

count = 0
while True:
    count += 1
    conn, addr = sock.accept()
    print(f"\nНовое подключение: {addr}\n")
    logging.info(f"Новое подключение: {addr}")
    Th = threading.Thread(target = user_input, args = (conn, addr))
    logging.info(f"Поток №{count}\n")
    Th.start()

conn.close()
