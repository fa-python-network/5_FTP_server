# -*- coding: utf-8 -*-
import socket, os, re, csv, logging
'''
pwd - показывает название рабочей директории
ls <dirname> - показывает содержимое директории
cat <filename> - отправляет содержимое файла
mkdir <dirname> - создает папку
rmdir <dirname> - удаляет папку
rename <oldfilename> <newfilename> - переименовывает файл
rm <filename> - удаляет файл
exit - отключается от сервера
'''

name = ''
user = []
udir = ''
logging.basicConfig(filename="serv.log", level=logging.INFO)

def login(nm, conn):
    global name
    name = nm
    
    with open ('users.csv', 'r') as f:
        know = False
        
        try:
            for line in csv.reader(f):
                print(line)
                if line[0].lower() == name.lower():
                    know = True
                    user = line
                    break
        
        except:
            pass
        
    if know:
        return user_known(user, conn)
    
    else:
        return user_unknown(name, conn)
        
    
def user_known(usr, conn):
    global user
    global udir
    user = usr
    mes = ''
    logging.info(f'Known {user[0]} came')
    
    while True:
        mes = mes + 'Введите пароль:'
        request = None
        
        conn.send(mes.encode())
        
        print("Прослушиваем порт", PORT)
        conn, addr = sock.accept()
        print(addr)
        
        request = conn.recv(1024).decode()
        print(request)
        
        if user[1] == request:
            logging.info(f'{user[0]} entered right password')
            udir = os.path.join(os.getcwd(), 'docs')
            break
        
        else:
            logging.info(f'{user[0]} entered wrong password')
            mes = 'Пароль неверный. '
    
    return conn
    
def user_unknown(name, conn):
    global udir
    global user
    logging.info(f'Unknown {user[0]} came')
    
    conn.send('Придумайте пароль:'.encode())
    
    print("Прослушиваем порт", PORT)
    conn, addr = sock.accept()
    print(addr)
    
    request = conn.recv(1024).decode()
    print(request)
    
    user.append(name)
    user.append(request)
    
    with open ("users.csv", "a", newline='') as inls:
        csv.writer(inls).writerow(user)
    
    udir = os.path.join(os.getcwd(), 'docs')
    os.mkdir(os.path.join(udir, name))
    return conn
    

def process(req, conn):
    global name
    global udir
    
    if '<Login is:>' in req:
        name = str(req.split()[2])
        return login(name, conn)
    
    elif req == 'pwd':
        return udir
    
    elif re.search(r'ls.*', req):
        try:
            if not '; '.join(os.listdir(os.path.join(udir, name, req[3:]))):
                return "Пустая папка"
            return ('; '.join(os.listdir(os.path.join(udir, name, req[3:]))))
        except:
            return 'Нет такой папки'
    
    elif re.search(r'cat .+', req):
        try:
            f = open(os.path.join(udir, name, req[4:]), 'r')
            return ' '.join([line for line in f])
        except:
            return 'No such file'
        
    elif re.search(r'mkdir .+', req):
        
        try:
            os.mkdir(os.path.join(udir, name, str(req.split()[1])))
            return str(req.split()[1]) + ' made'
        
        except:
            return 'Wrong path'
        
    elif re.search(r'rmdir .+', req):
        
        try:
            os.rmdir(os.path.join(udir, name, str(req.split()[1])))
            return str(req.split()[1]) + ' removed'
        
        except:
            return 'Wrong path'
        
    elif re.search(r'rm .+', req):
        
        try:
            os.remove(os.path.join(udir, name, str(req.split()[1])))
            return str(req.split()[1]) + ' removed'
        
        except:
            return 'Wrong path'
        
    elif re.search(r'rename .+ .+', req):
        
        try:
            os.rename(os.path.join(udir, name, str(req.split()[1])), os.path.join(udir, name, str(req.split()[2])))
            return str(req.split()[1]) + ' renamed to ' + str(req.split()[2])
        
        except:
            return 'Wrong path'
        
    elif req == 'exit':
        logging.info(f'{name} exited')
        return 'exit'
        
    return 'server'


PORT = 9990


sock = socket.socket()
sock.bind(('', PORT))
sock.listen(1)
logging.info("Server established. Socket's listening")

while True:
    name = ''
    user = []
    udir = ''
    
    print("Прослушиваем порт", PORT)
    conn, addr = sock.accept()
    print(addr)
    logging.info(f'{addr} connected')
    
    request = conn.recv(1024).decode()
    print(request)
    logging.info(f'Server got message: {request}')
    
    conn = process(request, conn)
    response = "Добро пожаловать, " + user[0]
    conn.send(response.encode())
    logging.info(f'{name} entered his directory')
    
    while True:
        print("Прослушиваем порт", PORT)
        conn, addr = sock.accept()
        print(addr)
        
        request = conn.recv(1024).decode()
        if request == 'exit':
            break
        else:
            print(request)
            logging.info(f'Server got message: {request}')
        
        response = process(request, conn)
        conn.send(response.encode())
    
sock.close()