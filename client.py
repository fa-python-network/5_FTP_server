import socket

HOST = 'localhost'
PORT = 1253
print("To exit print 'exit'")
while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())

    response = sock.recv(1024).decode()
    print(response)
    sock.close()
    if response == 'exit':
        print("Vi otrubili server nafig, tak chto vas mi tozhe virubaem :)")
        break
