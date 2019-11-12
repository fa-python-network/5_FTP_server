import os
import socket

def sendfile(name, who):
    with open(name, 'r') as file:
        for raw in file:
            who.send(raw.encode())
            who.recv(1024)
    who.send('end'.encode())

def checkfile(name, who):
    with open (name, 'w') as file:
        file.write(who.recv(1024).decode() + '\n')
        who.send('next'.encode())
