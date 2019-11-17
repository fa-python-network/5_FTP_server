import socket

HOST = 'localhost'
PORT = 6666

try:
    os.system('clear')
    os.system('cls')
except:
    pass


print('Для выхода введите команду exit')
print('Для справки введите команду help')

while True:
    request = input('>')
    if request == 'exit':
	    print('Клиент закрыт')
	    break
    elif request == 'help':
        print('''pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <directoryname> - создает директорию
rmdir <directoryname> - удаляет директорию
remove <filename> - удаляет путь к файлу
rename <filename> - переименовывает файл
copy <old name> <new name> - копирует файл''')
        

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
