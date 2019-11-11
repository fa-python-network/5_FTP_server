import socket


def cts(filename):
    with open(filename, 'rb') as f:
        a = f.read()
    sock.send(a)

def ctc():
    bytes = sock.recv(1024)


HOST = 'localhost'
PORT = 1260
print("To exit print 'exit'")
while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    if request[:4] == 'cts ':
        cts(request[4:])


    response = sock.recv(1024).decode()
    print(response)
    sock.close()
    if response == 'exit':
        print("Vi otrubili server nafig, tak chto vas mi tozhe virubaem :)")
        break
    if response == 'file':
        ctc()
