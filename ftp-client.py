import socket
import os
import getpass
import hashlib

HOST = "localhost"
PORT = int(input("Введите номер порта"))
userdir = os.path.join(os.getcwd(), "docs")

def verify_delete(path):
    deltype=tuple()
    fullpath=str()
    if os.path.isabs(path):
        fullpath = path
    else:
        fullpath = os.path.join(userdir,path)
    if os.path.isdir(fullpath):
        deltype=("a", "папка")
    else:
        deltype=("", "файл")
    print("Будет удален{} {} {}. Продолжить?".format(deltype[0],deltype[1],fullpath))
    answer=input()
    if str.lower(answer) in(["да","д","yes","y"]):
        return True
    else:
        return False

def check_user(username,file="users.txt"):
    """Проверка наличия пользователя в системе по данному IP-адресу"""
    log_in_successful=bool() 
    try:
        user_list=create_user_list(file) 
    except IOError as e: # если не удалось прочитать из файла, вывести сообщение об ошибке и создать его
        f=open(file,"w")
        f.close()
        print("Файл {} был создан!".format(file))
        log_in_successful=False
        user_list=create_user_list(file)
    finally:
        user_exists=False
        for user in user_list: 
            if username==user[1]: # если пользователь существует, спросить пароль и попробовать залогиниться
                entered_password=getpass.getpass("Введите пароль: ")
                while not log_in_user(username,entered_password):
                    log_in_successful=log_in_user(username, entered_password)
                user_exists=True
                break
        if not(user_exists): # если пользователя не существует, добавить
            name=input("Введите имя пользователя: ")
            password=getpass.getpass("Введите пароль: ")
            add_user(name, password, file)
            log_in_successful=True
    if log_in_successful:
        setup_user(username)
    return "Пользователь" + username + "вошёл в систему"

def setup_user(user):
    fullpath=os.path.join(os.getcwd(), user)
    if not os.path.exists(fullpath):
        os.mkdir(fullpath)
    userdir = fullpath
    current_user=user
    
def add_user(name,password,file="users.txt"):
    """Добавить пользователя с данным именем и паролем"""
    users_file=open(file,"a") #открывает файл на дозапись
    name.strip()
    password.strip() #удаляет лишние пробелы
    users_file.write("{};{}\n".format(name,encode(password)))
    print("Пользователь {} добавлен в систему".format(name))
    users_file.close()
    
def create_user_list(file="users.txt"):
    """Создаёт список с именами и паролями пользователей"""
    users_file=open(file,"r")
    user_list=list()
    for line in users_file: #читает записи из файла, разделяя поля по ; и добавляя в список
        user=line.split(";")
        user_list.append(user)
    return user_list
    users_file.close()
            
def log_in_user(user,entered_password):
    """Вход пользователя с паролем"""
    if(encode(entered_password)==user[2].strip()): #шифрование пароля и сравнение с паролем из файла
        print("Пользователь {} вошёл в систему".format(user[0]))
        return True
    else:
        print("Неверный пароль!")
        return False

def encode(password):
    """Безопасное хранение паролей"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
while True:
    request = input(">")

    sock = socket.socket()
    sock.connect((HOST, PORT))

    if request=="exit":
        break
    if request.split()[0] in ["rmdir","rm"]:
        if verify_delete(request.split()[1]):
            pass
        else:
            break
    if request.split()[0]=="login":
        pass
        #sock.send(check_user(request.split()[1].encode())
        
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
sock.close()
