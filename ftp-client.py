import socket
import os
import logging as log

host = 'localhost'


try:
    port= input("Здравствуйте! Введите номер порта: ")
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

print('''\n\nСписок доступных команд:
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <filename>  - создает новую папку
rmdir <filename>  - удаляет папку
touch <filename>  - создает файл
rm <filename>  - удаляет файл
rn <filename>  - переименовывает файл
copy <filename>  <newfilename> - копирует файл
exit - завершение работы(отключение клиента от сервера)''')

print("\n\nВведите команду.")
log.basicConfig(filename= 'file.log', format='%(levelname)s %(asctime)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=log.INFO)

while True:
    
    request = input('>')
    
    sock = socket.socket()
    sock.connect((host, port))

    
    if request != 'exit':
        sock.send(request.encode())
    else:
        print('Работа завершена.')
        log.info('Соединение завершено.')
        break

    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()