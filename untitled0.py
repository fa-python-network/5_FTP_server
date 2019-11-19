import socket
import os
import shutil

'''
pwd - название директории
ls - содержимое директории
cat <filename> - показать содержимое
cnd <name> - создает новую папку
deldir <name> - удаление папки
superdeldir <name> - принудительное удаление
cnf <name> - создает файл
delfile <name> - удаляет файл
pcf <name> - копирует файл на сервер
icf <name> - копирует файл с сервера
rename <name> <newname> - переименовывет файл
cquit - выход
'''
dirname = os.path.join(os.getcwd(), 'docs')

def proc(req):
    
    if req == 'help':
        return ('pwd - название директории\n'+
                'ls - содержимое директории\n' +
                'cat <filename> - показать содержимое\n' + 
                'cnd <name> - создает новую папку\n' +
                'deldir <name> - удаление папки\n' +
                'superdeldir <name> - принудительное удаление\n' +
                'cnf <name> - создает файл\n' +
                'delfile <name> - удаляет файл\n' +
                'pcf <name> - копирует файл на сервер\n' +
                'icf <name> - копирует файл с сервера\n' +
                'rename <name> <newname> - переименовывет файл\n' +
                'cquit - выход')
    
    if req == 'pwd':
        return dirname
    
    elif req == 'ls':
        return('; '.join(os.listdir(dirname)))
        
    elif req[:3] == 'cat':
        k = os.path.join(os.getcwd(), 'docs', req[4::])
        try:
            with open(k, 'r') as f:
                s = ''
                for i in f:
                    s += i
        except:
            return 'File is not foundded'
        return s
    
    elif req[:3] == 'cnd':
        k = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.isdir(k) == False:
            os.mkdir(k)
            return("Directory created")
        else:
            return("Directory already exist")
    
    elif req[:6] == 'deldir':
        k = os.path.join(os.getcwd(), 'docs', req[7::])
        try:
            os.rmdir(k)
        except:
            return("Directory is not empty")
        else:
            return("Directory deleted")
    
    elif req[:11] == 'superdeldir':
        k = os.path.join(os.getcwd(), 'docs', req[12::])
        shutil.rmtree(k, ignore_errors=False, onerror=None)
        return("Directory deleted")
        
    elif req[:3] == 'cnf':
        k = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.isfile(k) == False:
            try:
                f = open(k, 'w')
                f.close()
                return("File created")
            except:
                return("ERROR")
        else:
            return("File already exist")
            
    elif req[:7] == 'delfile':
        k = os.path.join(os.getcwd(), 'docs', req[8::])
        try:
            os.remove(k)
            return("File deleted")
        except:
            return("No such file in derictory")
            
    elif req[:3] == 'pcf':
        k = os.path.join(os.getcwd(), 'docs', req[4::])
        a = os.getcwd()
        try:
            shutil.copy(k, a)
            return("File copied on server")
        except:
            return("No such file in derictory")
            
    elif req[:3] == 'icf':
        k = os.path.join(os.getcwd(), 'docs')
        a = os.path.join(os.getcwd(), req[4::])
        try:
            shutil.copy(a, k)
            return("File copied from server")
        except:
            return("No such file in server")
            
    elif req[:6] == 'rename':
        try:
            a = req.split(" ")
            os.rename(os.path.join(os.getcwd(), 'docs', a[1]), os.path.join(os.getcwd(), 'docs', a[2]))
            return("File renamed")
        except:
            return("No such file in derictory")
            
    elif req == 'cquit':
        return req
            
    return 'Command is not founded'

port = 10000

sock = socket.socket()
sock.bind(('', port))
sock.listen()
print(port)

while True:
    conn, addr = sock.accept()
    
    req = conn.recv(1024).decode()
    print(req)
    
    res = proc(req)
    if res == 'cquit':
        conn.close()
    conn.send(res.encode())

conn.close()