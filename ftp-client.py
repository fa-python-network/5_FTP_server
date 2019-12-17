# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:53:25 2019

@author: Елизавета
"""

import socket
HOST = 'localhost'
PORT = 7576
description = 'Вам доступны следующие функции файлового менеджера:\npwd - отобразить название рабочей папки\nls - отобразить содержимое рабочей папки\ncat - отобразить содержимое файла\nmkdir - создать папку\nrm - удалить файл\nrmdir - удалить папку\ncp - копировать файл или папку\nmkfile - создать файл\neditf - редактировать файл\nmv - переименовать файл или папку\n\nДля начала введте start'
print(description)
start = input()
sock = socket.socket()
sock.connect((HOST, PORT))
sock.send(start.encode())
while True:
        
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    
    print(response)
    
sock.close()
