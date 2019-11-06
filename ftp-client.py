import socket
import os
import pickle
import time
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
        sock.send(pickle.dumps(["scp", request.split("/")[-1]]))
        time.sleep(0.3)
        with open(file, "rb") as f:
            data = f.read(1024)
            while data:
                sock.send(data)
                data = f.read(1024)
        sock.send(b"DONE")
    else:
        sock.send(pickle.dumps(request.split()))
    
    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()