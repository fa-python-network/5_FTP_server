import socket
import os
import csv
from datetime import datetime


#dirname = os.path.join(os.getcwd(), 'docs')

dirlevel = 0
def process(req):
    file=open('server.log', 'a')
    if req.split(' ')[0] == 'pwd':  # текущая директория
        pth=dirname.split('\\')
        file.write(f"выполнено: pwd({dirname}) ошибки: -\n")
        return "\\"+pth[-1]




    elif req.split(' ')[0] == 'ls':  # список файлов
        file.write(f"выполнено: ls({dirname}) ошибки: -\n")
        return '; '.join(os.listdir(dirname))

    elif req.split(' ')[0] == 'cat':  # содержимое файла
        if req.split(' ')[1] != '_eoc_':
            if os.path.exists(os.path.join(dirname, req.split(' ')[1])):
                with open(os.path.join(dirname, req.split(' ')[1]), 'r') as f:
                    return f.read()
                file.write(f"выполнено: cat({dirname}\\{req.split(' ')[1]}) ошибки: -\n")
            else:
                file.write("выполнено: cat ошибки: не найден файл \n")
                return 'no such file'
        else:
            file.write("выполнено: cat ошибки: пустой файл \n")
            return 'empty filename'

    elif req.split(' ')[0] == 'mkdir':
        if req.split(' ')[1] != '_eoc_':
            if os.path.exists(os.path.join(dirname, req.split(' ')[1])):
                file.write(f"выполнено: mkdir({dirname}\\{req.split(' ')[1]}) ошибки: файл(директория) уже существует \n")
                return 'dir (file) already exists!'
            else:
                os.mkdir(os.path.join(dirname, req.split(' ')[1]), 777)
                file.write(f"выполнено: mkdir({dirname}\\{req.split(' ')[1]}) ошибки: - \n")
                return f'Dir is created!'
        else:
            file.write(f"выполнено: mkdir() ошибки: отсутствует имя \n")
            return 'no filename'

    elif req[:5] == 'rmdir':
        if not os.listdir(f'{dirname}/{req[6:]}'):
            file.write(f"выполнено: rmdir({dirname}\\{req.split(' ')[1]}) ошибки: -\n")
            return os.rmdir(f'{dirname}\\{req[6:]}')
        else:
            file.write(f"выполнено: rmdir({dirname}\\{req.split(' ')[1]}) ошибки: не пустая директория\n")
            return 'Нельзя удалить эту директорию, т.к. в ней содержатся файлы!'

    elif req[:6] == 'remove':
        if req[7:] in os.listdir(f'{dirname}'):
            os.remove(f'{dirname}\\{req[7:]}')
            file.write(f"выполнено: remove({dirname}\\{req.split(' ')[1]}) ошибки: -\n")
            return 'Файл удален'
        else:
            file.write(f"выполнено: remove({dirname}\\{req.split(' ')[1]}) ошибки: файл или директория не существует\n")
            return 'Нет такого файла в текущей директории!'

    elif req.split(' ')[0] == 'rename':
        try:
            old_name=req.split()[1]
            new_name=req.split()[2]
            os.rename(old_name,new_name)
            return "Файл переименован"
        except OSError:
            return "Нет такого файла или директории!"
        except:
            return "Invalid value"


    file.close()
    return 'bad request'  # неправильный запрос


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(5)

while True:
    conn, addr = sock.accept()


    user = False
    names = open("data_names.csv", "a")
    names.close()
    names = open("data_names.csv", "r")
    for line in csv.reader(names):
        if line[0] == addr[0]:
            answer = "Введите пароль: "
            conn.send(answer.encode())
            while True:
                data = conn.recv(1024)
                password = data.decode()
                if line[2] == password:
                    answer = "Добро пожаловать, " + line[1] + "!"
                    try:
                        os.mkdir(os.path.join(os.getcwd(), f'{line[1]}'))
                        dirname = os.path.join(os.getcwd(), f'{line[1]}')
                    except OSError:
                        dirname = os.path.join(os.getcwd(), f'{line[1]}')
                    conn.send(answer.encode())
                    file = open('server_users.log', 'a')
                    file.write(f"{datetime.now()} Вход выполнен успешно: пароль верный.\n")
                    file.close()
                    break
                else:
                    conn.send("Неверный пароль. Попробуйте еще раз.".encode())
                    file = open('server_users.log', 'a')
                    file.write(f"{datetime.now()} неверный пароль.\n")
                    file.close()
            user = True
            file = open('server_users.log', 'a')
            file.write(f"{datetime.now()} Подключился известный пользователь\n")
            file.close()
            names.close()
            break
    if user == False:
        file = open('server_users.log', 'a')
        conn.send("Как Вас зовут?".encode())
        try:
            data = conn.recv(1024)
            name = data.decode()
            file.write(f"{datetime.now()} Добавлен пользователь " + name + "\n")
            conn.send("Придумайте пароль:".encode())
            data = conn.recv(1024)
            password = data.decode()
            file.close()
        except:
            name = "Гость"
            conn.send("Некорректный ввод данных! \nВыполнен вход как гостя.".encode())
            file.write(f"{datetime.now()} Пользователь выполнил вход как Гость\n")
            conn.send("Придумайте пароль:".encode())
            data = conn.recv(1024)
            password = data.decode()
            file.close()
        names = open("data_names.csv", "wt")
        csv.writer(names, delimiter=',').writerow([addr[0], name, password])
        names.close()
        answer = "Добро пожаловать, " + name + '!'
        '''
        '''
        try:
            os.mkdir(os.path.join(os.getcwd(), f'{name}'))
            dirname = os.path.join(os.getcwd(), f'{name}')
        except OSError:
            dirname = os.path.join(os.getcwd(), f'{name}')
        '''
        '''
        conn.send(answer.encode())


    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())

    conn.close()