# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:48:49 2019

@author: Елизавета
"""
import socket, os, shutil
'''
pwd - отобразить название рабочей папки
ls - отобразить содержимое рабочей папки
cat - отобразить содержимое файла
mkdir - создать папку
rm - удалить файл
rmdir - удалить папку
cp - копировать файл или папку
mkfile - создать файл
editf - редактировать файл
mv - переименовать файл или папку
'''
def process(request):
    global address
    if request == 'pwd':
        return 'localhost'+str(os.getcwd())[30:]
    
    
    elif request == ('ls'):
        print ("ls")
        return '; '.join(os.listdir())
    
    
    elif request[0:3] == 'cat':
        if request[4:13] == 'localhost':
            with open (address+request[13:], 'r') as f:
                return f.read()
        else:
            return 'У вас нет доступа к этим файлам'
        
        
    elif request[0:5] == 'mkdir':
        if request[6:15] == 'localhost': 
            try:
                os.mkdir(address+request[15:])
                return 'Выполнено: папка создана'
            except OSError:
                return 'Не выполнено: папка не создана'
        else:
            return 'У вас нет доступа к этим файлам'
        
        
    elif request[0:5] == 'rmdir':
        if request[6:15] == 'localhost': 
            try:
                os.rmdir(address+request[16:])
                return 'Выполнено: папка удалена'
            except OSError:
                return 'Не выполнено: папка не удалена. Возможно, в ней есть файлы. Удалите файлы, затем удалите папку.'
        else:
            return 'У вас нет доступа к этим файлам'
        
        
    elif request[0:2] == 'rm':
        if request[3:12] == 'localhost':
            try:
                os.remove(address+request[13:])
                return 'Выполнено: файл удален'
            except:
                return 'Не выполнено: файл не удален'
        else:
            return 'У вас нет доступа к этим файлам'
        
        
        
    elif request[0:2] == 'cp':
        if request[3:12] == 'localhost' && request.rfind('localhost') != 3:
            try:
                shutil.copyfile(address+request[13:].split()[0], address+request[(request.rfind('localhost')+10):])
                return 'Выполнено: файл скопирован'
            except:
                return 'Не выполнено: файл не скопирован'
        else:
            return 'У вас нет доступа к этим файлам'
        
        
        
    elif request[0:6] == 'mkfile':
        print(address+request[16:])
        try:
            if request[7:16] == 'localhost':   
                f = open(address+request[16:], 'w')
                
                return 'Выполнено: файл создан'
            else:
                return 'У вас нет доступа к этим файлам'
        except FileNotFoundError:
            return 'Не выполнено: файл или директория не найдены'
        
        
    elif request[0:5] == 'editf':
        if request[6:15] == 'localhost':
            try:
                with open(address+request[15:].split()[0], 'a') as f:
                    f.write(' '.join(address+request[15:].split()[1:]))
                    return 'Выполнено: данные записаны в файл'
            except:
                with open(address+request[15:].split()[0], 'w') as f:
                    f.write(' '.join(request[15:].split()[1:]))
                    return 'Выполнено: файл создан и данные записаны'
        else:
            return 'У вас нет доступа к этим файлам'
        
        
    elif request[0:2] == 'mv':
        if request[3:12] == 'localhost' && request.rfind('localhost') != 3:
            try:
                shutil.move(address+request[13:].split()[0], address+request[(request.rfind('localhost')+10):])
                return 'Выполнено: файл перемещен или переименован'
            except:
                return 'Не выполнено: файл не перемещен или не переименован'
        else:
            return 'У вас нет доступа к этим файлам'
        
        
    else:
        return 'server'
    
PORT = 7576
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
conn, addr = sock.accept()
for i in range(9999):
    try:
        os.mkdir('C:\\Users\\Елизавета\\Desktop\\ftp\\'+str(addr[0])+'.'+str(i))
        os.chdir('C:\\Users\\Елизавета\\Desktop\\ftp\\'+str(addr[0]+'.'+str(i)))
        address = 'C:\\Users\\Елизавета\\Desktop\\ftp\\'
        break
    except FileExistsError:
        pass
request = conn.recv(1024).decode()
response = process('Добро пожаловать!')
while True:
    print("Прослушивается порт " + str(PORT))
    
    conn, addr = sock.accept()
    print(addr)
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

sock.close()
input()