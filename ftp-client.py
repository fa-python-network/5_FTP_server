import socket

HOST = 'localhost'
PORT = 6670

while True:
    request = input('>')
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
