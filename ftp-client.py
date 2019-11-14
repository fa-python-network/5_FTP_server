import socket
import os
import getpass
import hashlib

HOST = "localhost"
PORT = int(input("Введите номер порта"))
global userdir
global current_user
userdir = os.path.join(os.getcwd(), "docs")
current_user=""

def verify_delete(path):
    global userdir
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
            if username==user[0]: # если пользователь существует, спросить пароль и попробовать залогиниться
                user_exists=True
                while True:
                    entered_password=getpass.getpass("Введите пароль: ")
                    log_in_successful=log_in_user(user, entered_password)
                    if log_in_successful: break
                break
        if not(user_exists): # если пользователя не существует, добавить
            password=getpass.getpass("Введите пароль: ")
            add_user(username, password, file)
    setup_user(username)


def setup_user(user):
    """Сделать папку пользователя текущей userdir и польхователя текущим пользователем """
    global userdir
    global current_user
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
    if(encode(entered_password)==user[1].strip()): #шифрование пароля и сравнение с паролем из файла
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
        check_user(request.split()[1])
        
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
sock.close()
