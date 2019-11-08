import socket

HOST = 'localhost'
PORT = 6662

while True:
    request = input('>')
    req = request.split()
    sock = socket.socket()
    sock.connect((HOST, PORT))

    if (req[0] == 'CtS'):
        qw = req[0] + ' ' + req[1]
        print(qw)
        sock.send(qw.encode())
        response = sock.recv(1024).decode()
        if response == "OK":
            f = open(req[2], 'rb')
            l = f.read(1024)
            while (l):
                sock.send(l)
                l = f.read(1024)
            sock.send('END'.encode())
        else:
            print('Error')
    else:
        sock.send(request.encode())

    response = sock.recv(1024).decode()
    print(response)
    
    sock.close()