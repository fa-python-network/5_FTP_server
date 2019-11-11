import socket


def cts(filename):
    with open(filename, 'rb') as f:
        a = f.read()
    sock.send(a)


def ctc():
    filename = sock.recv(1024).decode()
    print(filename)
    a = b''
    while True:
        data = sock.recv(1024)
        a += data
        if not data:
            break
    with open(filename, 'wb') as f:
        f.write(a)


HOST = 'localhost'
PORT = 1262
print("To exit print 'exit'")
while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    if request[:4] == 'cts ':
        cts(request[4:])

    response = sock.recv(1024).decode()
    if response == 'file':
        ctc()
    print(response)
    sock.close()
    if response == 'exit':
        print("Vi otrubili server nafig, tak chto vas mi tozhe virubaem :)")
        break
