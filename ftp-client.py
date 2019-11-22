import socket
PORT = 8888
HOST = 'localhost'

while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())

    response = sock.recv(1024).decode()
    print(response)
    sock.close()
