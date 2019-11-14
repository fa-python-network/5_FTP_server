import socket
import os
import shutil
from datetime import datetime
"""
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <path> - создаёт папку
rmdir <path> - удаляет папку
rm <filename> - удалить файл
rename <old filename> <new filename> - переименовать файл
copycs <filename from> <filename to>
copysc <filename from> <filename to>
exit (отключение) реализовано на клиенте
login <user> 
"""

userdir = os.path.join(os.getcwd(), "docs") #директория по умолчанию
current_user=""

def check_access(path):
    """Проверяет, есть ли доступ у пользователя к этой директории """
    fullpath = str() 
    if os.path.isabs(path):
        fullpath = path
    else:
        fullpath = os.path.join(userdir,path)
    if userdir in fullpath:
        return True
    else:
        print("Доступ запрещён!")
    return False

def pwd():
    """Возвращает директорию пользователя """
    return userdir

def ls(path):
    """Возвращает содержимое директории """
    return "Содержимое директории:\n" + "; ".join(os.listdir(path))

def cat(filename):
    """Возвращает содержимое файла """
    fullpath = str()
    content = str()
    if os.path.isabs(filename):
        fullpath = filename
    else:
        fullpath = os.path.join(userdir,filename)
    with open(fullpath, "r") as f:
        for line in f:
            content+=line
    return "Содержимое файла " + fullpath + ":\n" + content
    
def mkdir(path):
    """Создаёт директорию """
    if check_access(path):
        fullpath = os.path.join(userdir,path)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
            return "Создана папка " + fullpath
    return "Ошибка доступа к директории " + path

def rmdir(path):
    if check_access(path):
        fullpath = os.path.join(userdir,path)
        if os.path.exists(fullpath):
            shutil.rmtree(fullpath)
            return  "Удалена папка " + fullpath
    return "Ошибка доступа к директории " + path

def rm(filename):
    if check_access(filename):
        fullpath = os.path.join(userdir,filename)
        if os.path.exists(fullpath):
            os.remove(fullpath)
            return "Удалён файл " + fullpath
    return "Ошибка доступа к директории " + path
    
def copycs(filename_from,filename_to):
    if filename_to is None:
        filename_to=os.path.join(user_dir,os.path.basename(filename_from))
    if os.path.isabs(filename_from):
        filename_from=os.path.join(userdir,filename_from)
    if os.path.isabs(filename_to):
        filename_to=os.path.join(os.getcwd(),filename_to)
    shutil.copyfile(filename_from, filename_to)

def copysc(filename_from, filename_to):
    if filename_to is None:
        filename_to=os.path.join(user_dir,os.path.basename(filename_from))
    if not os.path.isabs(filename_from):
        filename_from=os.path.join(os.getcwd(),filename_to)
    if not os.path.isabs(filename_to):
        filename_to=os.path.join(userdir,filename_from)
    shutil.copyfile(filename_from, filename_to)
    
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

def man(command):
    pass

def process(req):
    res= ""
    if req == "pwd":
        res = pwd()
    elif req == "ls":
        res = ls(userdir)
    elif req.split()[0]=="cat":
        res = cat(req.split()[1])
    elif req.split()[0]=="mkdir":
        res = mkdir(req.split()[1])
    elif req.split()[0]=="rmdir":
        res = rmdir(req.split()[1])
    elif req.split()[0]=="rm":
        res = rm(req.split()[1])
    elif req.split()[0]=="copycs":
        res = copycs(req.split()[1],req.split()[2])
    elif req.split()[0]=="copysc":
        res = copycs(req.split()[1],req.split()[2])
    elif req.split()[0]=="login":
        res=check_user(req.split()[1])
    elif req.split()[0]=="map":
        res=map(req.split()[1])
    else:
        res="bad request"
    return res

def log(message,file):
    if os.path.exists(os.path.join(os.getcwd(),file)):
        mod="a"
    else:
        mod="w+"
        with open(file,mod) as f:
            f.write(datetime.now() + ": "+ message+"\n")


PORT = 6666

sock = socket.socket()
sock.bind(("", PORT))
sock.listen()
print("Прослушиваем порт ", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())
    log(response,"log.txt")

    conn.close()
