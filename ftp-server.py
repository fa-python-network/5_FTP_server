import socket
import os 
import shutil
#import Image
'''
name.me - название директории
vol.me - содержимое директории
look <filename> - показать содержимое
cnd <name> - создает новую папку
deldir <name> - удаление папки
prindeldir <name> - принудительное удаление
cnf <name> - создает файл
delfile <name> - удаляет файл
pcf <name> - копирует файл на сервер
icf <name> - копирует файл с сервера
rename <name> <newname> - переименовывет файл
quit - выход
'''
dirname = os.path.join(os.getcwd(), 'docs')

def proc(request):
    if request == 'name.me':
        return dirname
    
    elif request == 'vol.me':
        return('; '.join(os.listdir(dirname)))
        
    elif request[:4] == 'look':
        k = os.path.join(os.getcwd(), 'docs', request[5::])
        try:
            with open(k, 'r') as f:
                s = ''
                for i in f:
                    s += i
        except:
            return 'File is not foundded'
        return s
    
    elif request[:3] == 'cnd':
        k = os.path.join(os.getcwd(), 'docs', request[4::])
        if os.path.isdir(k) == False:
            os.mkdir(k)
            return("Directory created")
        else:
            return("Directory already exist")
    
    elif request[:6] == 'deldir':
        k = os.path.join(os.getcwd(), 'docs', request[7::])
        try:
            os.rmdir(k)
        except:
            return("Directory is not empty")
        else:
            return("Directory deleted")
    
    elif request[:11] == 'daddydeldir':
        k = os.path.join(os.getcwd(), 'docs', request[12::])
        shutil.rmtree(k, ignore_errors=False, onerror=None)
        return("Directory deleted")
        
    elif request[:3] == 'cnf':
        k = os.path.join(os.getcwd(), 'docs', request[4::])
        if os.path.isfile(k) == False:
            try:
                f = open(k, 'w')
                f.close()
                return("File created")
            except:
                return("ERROR")
        else:
            return("File already exist")
            
    elif request[:7] == 'delfile':
        k = os.path.join(os.getcwd(), 'docs', request[8::])
        try:
            os.remove(k)
            return("File deleted")
        except:
            return("No such file in derictory")
            
    elif request[:3] == 'pcf':
        k = os.path.join(os.getcwd(), 'docs', request[4::])
        a = os.getcwd()
        try:
            shutil.copy(k, a)
            return("File copied on server")
        except:
            return("No such file in derictory")
            
    elif request[:3] == 'icf':
        k = os.path.join(os.getcwd(), 'docs')
        a = os.path.join(os.getcwd(), request[4::])
        try:
            shutil.copy(a, k)
            return("File copied from server")
        except:
            return("No such file in server")
            
    elif request[:6] == 'rename':
        try:
            a = request.split(" ")
            os.rename(os.path.join(os.getcwd(), 'docs', a[1]), os.path.join(os.getcwd(), 'docs', a[2]))
            return("File renamed")
        except:
            return("No such file in derictory")
            
    elif request == 'quit':
        return request
            
        
    return 'Command is not found'

PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print(PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = proc(request)
    if response == 'quit':
        conn.close()
    conn.send(response.encode())

conn.close()