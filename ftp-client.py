import socket

print("*****")
print("pwd - текущая директория")
print("ls - содержимое текущей директории")
print("cat <filename> - содержимое файла")
print("mkdir <dirname> - создать новую директорию")
print("rmdir <dirname> - удалить пустую директорию")
print("create <filename> <text> - создать файл, записывать текст в файл,\nесли он передан после имени файла")
print("remove <filename> - удалить файл")
print("rename <oldfilename> <newfilename> - переименовать файл")
print("*****")

HOST = 'localhost'
PORT = 9090

while True:
    request = input('Введите команду:')

    sock = socket.socket()
    sock.connect((HOST, PORT))

    sock.send(request.encode())

    response = sock.recv(1024).decode()
    print(response)

    sock.close()