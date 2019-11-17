import socket

print("----------------")
print("pwd - текущая директория")
print("ls - содержимое текущей директории")
print("cat <filename> - содержимое файла")
print("mkdir <dirname> - создать новую директорию")
print("rmdir <dirname> - удалить пустую директорию")
print("create <filename> <text> - создать файл, записывать текст в файл,\nесли он передан после имени файла")
print("remove <filename> - удалить файл")
print("rename <oldfilename> <newfilename> ")
print("copy_to_server <filename1> <filename2> - Скопировать файл с клиента на сервер")
print("copy_from_server <filename1> <filename2> - Скопировать файл с сервера на клиент")
print("exit - выход")
print("----------------")

HOST = 'localhost'
PORT = 6666

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())

    if request == 'exit':
        sock.close()
        print('Соединение прервано')
        break
    
    response = sock.recv(1024).decode()
    print(response)
    
sock.close()