import socket
import os
import shutil
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
"""

userdir = os.path.join(os.getcwd(), "docs")
    
def check_access(path):
    fullpath = str()
    if os.path.isabs(path):
        fullpath = path
    else:
        fullpath = os.path.join(userdir,path)
    if userdir in fullpath:
        return True
    return False

def pwd():
    return userdir

def ls(path):
    return "Содержимое папки:\n" + "; ".join(os.listdir(path))

def cat(filename):
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
    if check_access(path):
        fullpath = os.path.join(userdir,path)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
            return "Создана папка " + fullpath
    return "Ошибка"

def rmdir(path):
    if check_access(path):
        fullpath = os.path.join(userdir,path)
        if os.path.exists(fullpath):
            shutil.rmtree(fullpath)
            return  "Удалена папка " + fullpath

def rm(filename):
    if check_access(filename):
        fullpath = os.path.join(userdir,filename)
        if os.path.exists(fullpath):
            os.remove(fullpath)
            return "Удалён файл " + fullpath
    
def copycs(filename_from,filename_to):
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
    else:
        res="bad request"
    return res

def log(message,file):
    if os.path.exists(os.path.join(os.getcwd(),file)):
        with open(file,"a") as f:
            f.write(message+"\n")
    else:
        with open(file,"w+") as f:
            f.write(message+"\n")

PORT = 6666

sock = socket.socket()
sock.bind(("", PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())
    log(response,"log.txt")

conn.close()
