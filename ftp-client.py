import socket

PORT = 9090
HOST = "localhost"
while True:
    request = input('> ')

    sock = socket.socket()
    sock.connect((HOST, PORT))

    sock.send(request.encode())

    if request == 'exit':
        sock.close()
        print('EXIT')
        break
    
    response = sock.recv(1024).decode()
    print(response)

    sock.close()