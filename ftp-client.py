import socket
import os

HOST = "localhost"
PORT = 6666
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
    
    
while True:
    request = input(">")
    
    if request=="exit":
        break
    if request.split()[0] in ["rmdir","rm"]:
        if verify_delete(request.split()[1]):
            pass
        else:
            break
        
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
sock.close()