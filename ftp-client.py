# -*- coding: utf-8 -*-
import socket
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir - 
rmdir - 
rename - 
'''

HOST = 'localhost'
PORT = 9990

print('Введите логин:')
lgd = False
pswd = False

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    if not lgd:
        name = request
        request = '<Login is:> ' + request
        sock.send(request.encode())
        lgd = True
        
    else:
        sock.send(request.encode())    
     
    try:
        response = sock.recv(1024).decode()
    except:
        pass


    
    print(response)
    
    sock.close()