import socket

'''
pwd - показывает название рабочей директории
ls - содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <Название папки> - создает новую папку
rmdir <Название папки> - удаляет папку
create <Название файла> - создает файл
remove <Название файла> - удаляет файл
rename <Название файла> - переименовывает файл
copy <Название файла> <Название нового файла> - копирует файл
'''

HOST = 'localhost'
PORT = 6666

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()