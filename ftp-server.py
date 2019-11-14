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

def change_port(port,server_socket):
    """Проверка, занят ли порт с этим сокетом. При занятости порта происходит его инкремент."""
    while(True):
        try:
            server_socket.bind(('',port))
        except socket.error:
            port+=1
        else:
            break
    return port

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
        res=conn.recv(1024).decode()
    else:
        res="bad request"
    return res

def log(message,file):
    if os.path.exists(os.path.join(os.getcwd(),file)):
        mod="a"
    else:
        mod="w+"
        with open(file,mod) as f:
            f.write(str(datetime.now()) + ": "+ message+"\n")

sock = socket.socket()
port = change_port(int(input("Введите номер порта")),sock)
sock.listen()
print("Прослушиваем порт ", port)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())
    log(response,"log.txt")

conn.close()
