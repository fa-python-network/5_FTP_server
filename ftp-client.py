import socket
import os

HOST = 'localhost'
PORT = 6666


print('\nДля получения списка команд введите команду help')
print('Для выхода введите команду exit\n')

while True:
    request = input('>')
    if request == 'exit':
        print('Клиент закрыт')
        break
    
    elif request == 'help':
        print('''
pwd - показывает название рабочей директории
ls - содержимое текущей директории
cat <Название папки> - отправляет содержимое файла
mkdir <Название папки> - создает новую папку
rmdir <Название папки> - удаляет папку
create <Название файла> - создает файл
remove <Название файла> - удаляет файл
rename <Название файла> - переименовывает файл
copy <Название файла> <Название нового файла> - копирует файл
get <Название файла> - скачать с сервера файл
push <Название файла> - загрузить на сервер файл
exit - закрыть клиент
help - помощь
''')
    else:
        sock = socket.socket()
        sock.connect((HOST, PORT))
        if request.split(' ')[0] == 'push':
            request+=' _eoc_'
            if request.split(' ')[1] != '_eoc_':
                if '..' in request.split(' ')[1] or '/' in request.split(' ')[1] or '\\' in request.split(' ')[1]:
                    print('Не допускается использование .. / \\')
                else:
                    if os.path.exists(request.split(' ')[1]):
                        if os.path.isfile(request.split(' ')[1]):
                            sock.send(request.encode())
                            with open(request.split(' ')[1],'r') as f:
                                forsend = f.read().encode()
                            sock.send(forsend)
                            answer = sock.recv(1024)
                            print(answer.decode())
                        else:
                            print('Это не файл')
                    else:
                        print('Такого файла нет')
            else:
                print('Вы забыли ввести название файла')

        else:
            sock.send(request.encode())
            response = sock.recv(1024).decode()
            if request.split(' ')[0] == 'get':
                if response.split('-!-!-!->')[0] == 'success':
                    with open(request.split(' ')[1],'w') as f:
                        f.write(response.split('-!-!-!->')[1])
                    print('Готово')
                else:
                    print(response)
            else:
                print(response)
        
        
        sock.close()
