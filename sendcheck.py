import os
import socket
from time import sleep


def sendfile(name, who):
    with open(name, 'r') as file:
        for raw in file:
            who.send(raw.encode())
            who.recv(1024)
    who.send('end'.encode())

def checkfile(name, who, maindir, usname):
    while True:
        msg = who.recv(1024).decode()
        if msg == 'end':
            return True
        elif get_size(maindir+f'/{usname}') > 10240:
            return False
        else:
            with open (name, 'a') as file:
                file.write(msg)
                sleep(0.001)
                who.send('next'.encode())


def get_size(start_path):  # Стырена в тырнетах с:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
    