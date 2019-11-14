import socket, os
from datetime import datetime


print("**************************")
print("pwd - текущая директория")
print("ls - содержимое текущей директории")
print("cat - содержимое файла")
print("mkdir <name> - создать новую директорию")
print("rmdir <name> - удалить пустую директорию")
print("remove <name> - удалить файл")
print("rename <old> <new> - изменить имя (почему то не работает :( )")
print("exit - выход")
print("**************************")
HOST = 'localhost'
PORT = 6666
sock = socket.socket()
sock.connect((HOST, PORT))
while True:
    data = sock.recv(1024)
    print(data.decode())

    if data.decode() == "Как Вас зовут?":
        name = input()
        sock.send(name.encode())

    if data.decode() == "Придумайте пароль:":
        password = input()
        if password != "":
            sock.send(password.encode())

    if data.decode() == "Введите пароль: " or data.decode() == "Неверный пароль. Попробуйте еще раз.":
        password = input()
        sock.send(password.encode())

    if "Добро пожаловать" in data.decode():
        break

while True:
    request = input('>')
    file = open('server.log', 'a')
    file.write(f"{datetime.now()} соединение установлено \n \n")
    file.close()
    if request == 'exit':
        file=open('server.log','a')
        file.write(f"{datetime.now()} закрыто соединение \n \n")
        print('Клиент закрыт')
        file.close()
        break

    else:


        sock.send(request.encode())

        response = sock.recv(1024).decode()
        print(response)

sock.close()