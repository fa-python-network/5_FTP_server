import socket
import os
import pickle

HOST = 'localhost'
PORT = int(input("Введите порт:"))
while True:
    request = input('>')
    sock = socket.socket()
    sock.connect((HOST, PORT))
    if request.lower() == "exit":
        sock.close()
        break
    elif request.lower().split()[0] == "scp":
        file = os.path.realpath(request.split()[1])
        with open(file, "rb") as f:
            sock.send(pickle.dumps(["scp", f, request.split("/")[-1]]))

    sock.send(request.encode())
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()