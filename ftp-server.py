import socket
import os
import shutil
import logging as log
import json
from datetime import datetime

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <filename>  - создает новую папку
rmdir <filename>  - удаляет папку
touch <filename>  - создает файл
rm <filename>  - удаляет файл
rn <filename>  - переименовывает файл
copy <filename>  <newfilename> - копирует файл
exit
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        log.info("Вызвана команду pwd.")
        return dirname
    
    elif req == 'ls':
        log.info('Вызвана команду ls.')
        return '; '.join(os.listdir(dirname))
    
    elif 'cat' in req:
        path = os.path.join(os.getcwd(), 'docs', req[4::])
        log.info('Вызвана команда cat.')
        if os.path.exists(path):
            with open(path, 'r+') as f:
                line = ''
                for l in f:
                    line+=l
            return line
        else:
            log.info('Команда cat не выполнена.')
            return 'Данного файла не существует.'
    
    elif 'mkdir' in req:
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        log.info('Вызвана команда mkdir.')
        if not os.path.exists(path):
            os.makedirs(path)
            return 'Директория создана.'
        else: 
            log.info('Команда mkdir не выполнена.')
            return 'Данная директория уже существует.'
    
    elif 'rmdir' in req:
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        log.info('Вызвана команда rmdir.')
        if os.path.exists(path):
            shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6::]))
            return 'Директория удалена.'
        else: 
            log.info('Команда rmdir не выполнена.')
            return 'Данная директория не существует.'
            
    elif 'touch' in req:
        t = ''
        log.info('Вызвана команда touch.')
        with open(os.path.join(os.getcwd(), 'docs', req[6::]), 'tw', encoding='utf-8') as f:
            f.write(t)
        return 'Файл создан.'

    elif 'rm' in req:
        log.info('Вызвана команда rm.')
        os.remove(os.path.join(os.getcwd(), 'docs', req[3:]))
        return 'Файл удален.'

    elif 'rn' in req:
        log.info('Вызвана команда rn.')
        req = req.split(' ')
        os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл переименован.'

    elif 'copy' in req:
        log.info('Вызвана команда copy.')
        req = req.split(' ')
        shutil.copyfile(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл скопирован.'

    return 'Ошибка в запросе. Повторите еще раз.'


log.basicConfig(filename= 'file.log', format='%(levelname)s %(asctime)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=log.INFO)
log.info('Соединение установлено.')

sock = socket.socket()

try:
    port= input("Введите номер порта: ")
    if port == '':
        port = 9090
    port = int(port)
    if type(port) == int and 0 <= port <= 65535:
        pass
    else:
        port = 9090
except ValueError:
    port = 9090
    print("Введен некорректный порт. По умолчанию - 9090.")

sock.bind(('', port))
sock.listen()
print("Прослушиваем порт", port)


while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    
    conn.send(response.encode())


conn.close()
