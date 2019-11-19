import socket
from datetime import datetime

sock = socket.socket()
sock.setblocking(1)
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

while True:
    HOST = input('Введите адрес хоста или localhost : \n')
    if HOST == 'localhost':
        HOST = '127.0.0.1'
        break
    host_l = HOST.split('.')
    if (0 < int(host_l[0]) < 255) and (0 < int(host_l[1]) < 255) and (0 < int(host_l[2]) < 255) and (
            0 < int(host_l[3]) < 255):
        break
    else:
        print('Введен неверный формат адреса.')
while True:
    PORT = input('Введите номер порта от 1024 до 49151: \n')
    if 1023 < int(PORT) < 49152:
        break
    else:
        print('Неверный номер порта.')
        break


sock.connect((HOST, int(PORT)))
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

msg = ""
while msg != 'exit':
    msg = input('>')
    file = open('server.log', 'a')
    file.write(f"{datetime.now()} соединение установлено \n \n")
    file.close()
    if msg == 'exit':
        file=open('server.log','a')
        file.write(f"{datetime.now()} закрыто соединение \n \n")
        print('Клиент закрыт')
        file.close()
    sock.send(msg.encode())
    data = sock.recv(1024)
    print(data.decode())

sock.close()
