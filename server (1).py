import socket
import os
import shutil

"""
pwd - сервер вернёт название рабочей директории
ls - сервер вернёт список файлов в рабочей директории
cat - сервер вернёт содержимое файла
mkdir - сервер создаёт директорию с указанным именем
rmdir - сервер удаляет директорию с указанным именем
rm - сервер удаляет файл с указанным именем
touch - сервер создаёт файл с указанным именем
rename - сервер переименновывает файл с указанным именем 
send - сервер ПОЛУЧАЕТ файл от клинета
recv - сервер ОТПРАВЛЯЕТ файл клинету
(называть команды такими именами удобнее для клиента)
cd - переход в указанную директорию
"""


def size(name):
    """Считает размер папки пользователя, не может использоваться как запрос"""
    path = home + f'\\{name}'
    result = 0
    for directory, subdirectory, files in os.walk(path):
        if files:
            for file in files:
                path = directory + f'\\{file}'
                result += os.path.getsize(path)
    return result


def pwd():
    """Возвращает текущую директорию"""
    if name == 'admin':
        return os.getcwd()
    return os.getcwd()[len_home:]


def ls():
    """Возвращает все элементы текущей директории"""
    return ' '.join(os.listdir(os.getcwd()))


def cat(name):
    """Показывает содержимое файла"""
    with open(name, 'r') as file:
        return file.read()


def mkdir(name):
    """Создаёт пустую директорию"""
    path = os.getcwd() + '\\' + name
    os.mkdir(path)
    return f'папка {name} успешно создана'


def rmdir(name):
    """Удаляет директорию НАХОДЯЩУЮСЯ В ТЕКУЩЕЙ ДЕРИКТОРИИ"""
    path = os.getcwd() + '\\' + name
    shutil.rmtree(path)
    return f'папка {name} успешно удалена'


def rm(name):
    """Удаляет файл"""
    path = os.getcwd() + '\\' + name
    os.remove(path)
    return f'файл {name} успешно удалён'


def touch(name):
    """Создаёт пустой файл"""
    with open(name, 'w') as file:
        pass
    return f'файл {name} успешно создан'


def cd(path):
    """в качестве параметра можно передавать только относительный путь, состоящий из названия директории в которую
    перейти иди символов '..' """
    if path == '..':
        if os.getcwd() == home_directory:
            return 'Вы в корневой директории'
        directory = '\\'.join(os.getcwd().split('\\')[:-1])
    else:
        directory = '\\'.join(os.getcwd().split('\\')) + '\\' + path
    os.chdir(directory)
    return f'Текущая директория {pwd()}'


def rename(name1, name2):
    """Переименновывает файл"""
    os.rename(name1, name2)
    return f'файл {name1} успешно переименнован в {name2}'


def send(name, conn, userr):
    """Получает файл от клиента"""
    length = conn.recv(1024).decode()
    text = conn.recv(int(length)).decode()
    with open(name, 'w') as file:
        file.write(text)
    # Это единственная команда, которая увеличивает размер пользовательской директории
    # Если бы таких команд было бы больше, код ниже выносился бы в функцию, которая регулярно вызывалась
    if userr != 'admin':
        if size(userr) > max_size:
            rm(name)
            return 'Недостаточно места на диске'
    return f'получен файл {name}'


def recv(name, conn):
    """Отправляет файл клиенту"""
    with open(name, 'r') as file:
        text = file.read()
    conn.send(str(len(text)).encode())
    conn.send(text.encode())
    return f'отправлен файл {name}'


def new_user(conn, user):
    """Добавление нового пользователя в файл users.txt"""
    name = conn.recv(1024).decode()
    # Проверка незанятости имени
    if name not in user.keys():
        conn.send('1'.encode())
        password = conn.recv(1024).decode()
        user[name] = user.get(name, password)
        file = home + '\\users.txt'
        with open(file, 'w') as users:
            print(user, file=users)
        mkdir(name)
        return name
    else:
        conn.send('0'.encode())
        flag2 = conn.recv(1024).decode()
        if int(flag2):
            # Как и почему это должно писаться я понял очень смутно
            # Но без этого может возвращаться пустое имя
            name = old_user(conn, user)
            return name
        else:
            name = new_user(conn, user)
            return name


def old_user(conn, users):
    """Проверка пароля при входе старого пользователя"""
    name = conn.recv(1024).decode()
    # Проверка есть ли такое имя
    if name in users.keys():
        conn.send('1'.encode())
        passwd = users[name]
        while True:
            password = conn.recv(1024).decode()
            if passwd == password:
                conn.send('0'.encode())
                return name
            else:
                conn.send('1'.encode())
    else:
        conn.send('0'.encode())
        flag2 = conn.recv(1024).decode()
        if int(flag2):
            name = new_user(conn, users)
            return name
        else:
            name = old_user(conn, users)
            return name


# Обработка запроса клиента
def process(req, args=None):
    # Пытаемся выполнить функцию из запроса
    try:
        f = commands[req]
    # Если такой функции нет возвращаем сообщение об этом
    except KeyError:
        return f"Команда {req} отсутствует"
    if args:
        return f(*args)
    return f()


# словарь всех возможных действий на сервере
commands = {'pwd': pwd, 'ls': ls, 'mkdir': mkdir, 'rmdir': rmdir, 'rm': rm, 'touch': touch, 'rename': rename,
            'send': send, 'recv': recv, 'cat': cat, 'cd': cd}

PORT = 9090

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

home = os.getcwd()  # Стартовая директория, в которой лежит сервер и будут создаваться домашние директории пользователей
len_home = len(home)  # Её размер
log = home + '\\log.txt'
max_size = 500  # Максимальный размер директории каждого пользователя в байтах

with open(log, 'a', encoding="UTF-8") as logs:
    print(f"Слушаем порт {PORT}", file=logs)

user = {'admin': 'Blagoveshensk - luchshiy gorod'}
# Пытаемся прочесть данные из файла и преобразовать их в словарь
try:
    with open('users.txt', 'r') as users:
        user = eval(users.read())
# Если файла нет: создаём его, список юзеров - пустой словарь
except FileNotFoundError:
    with open('users.txt', 'w') as users:
        pass
# Если файл пустой: список юзеров - пустой словарь
except SyntaxError:
    pass

while True:
    # Обновляем домашнюю директорию
    home_directory = home
    conn, addr = sock.accept()
    with open(log, 'a', encoding="UTF-8") as logs:
        print(f"Подключился {addr}", file=logs)

    # Получаем имя пользователя
    flag = int(conn.recv(1).decode())
    if flag:
        name = new_user(conn, user)
        with open(log, 'a', encoding="UTF-8") as logs:
            print(f"Зарегестрировался пользователь {name}", file=logs)
    else:
        name = old_user(conn, user)
        with open(log, 'a', encoding="UTF-8") as logs:
            print(f"Вошёл пользователь {name}", file=logs)

    conn.send(f"Hello, {name}".encode())

    if name != "admin":
        # Получаем домашнюю директорию для пользователя за пределы которой он не выйдет
        home_directory += f'\\{name}'
    # И перемещаемся в неё
    path = '\\'.join(home_directory.split('\\'))
    os.chdir(path)

    while True:

        request = conn.recv(1024).decode()
        request = request.split()
        if not request:
            break
        func = request[0]
        if len(request) > 0:
            args = request[1:]
        else:
            args = None
        if args:
            if func in ['send', 'recv']:
                args.append(conn)
                if func == 'send':
                    args.append(name)
            response = process(func, args)
        else:
            response = process(func)
        with open(log, 'a', encoding="UTF-8") as logs:
            print(f"Запрос {func} от пользователя {name}", file=logs)
        conn.send(response.encode())
    conn.close()

sock.close()
