import socket

print("*************** Доступные команды ***************")
print("pwd - название текущей директории")
print("ls - содержимое текущей директории")
print("cat <filename> - содержимое файла")
print("mkdir <dirname> - создать новую директорию")
print("rmdir <dirname> - удалить пустую директорию")
print("create <filename> <text> - создать файл, записать в него текст <text>")
print("remove <filename> - удалить файл")
print("rename <oldfilename> <newfilename> - переименовать файл")
print("copy_to_server <filename1> <filename2> -  отправить файл с клиента на сервер")
print("copy_from_server <filename1> <filename2> - скачать файл с сервера на клиент")
print("exit - выход")


HOST = 'localhost'
PORT = 6666

@@ -11,6 +25,11 @@

    sock.send(request.encode())

    if request == 'exit':
      sock.close()
      print('Соединение прервано')
      break

    response = sock.recv(1024).decode()
    print(response)
