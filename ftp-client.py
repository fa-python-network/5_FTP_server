import socket

HOST = 'localhost'
PORT = 6666

try:
    os.system('clear')
    os.system('cls')
except:
    pass

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
exit - закрыть клиент
help - помощь
''')
	else:
	    sock = socket.socket()
	    sock.connect((HOST, PORT))
	    sock.send(request.encode())

	    response = sock.recv(1024).decode()
	    print(response)

	    sock.close()
        