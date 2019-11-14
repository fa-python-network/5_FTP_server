import socket


def send_file(name, sock):
    sock.send(f'send {name}'.encode())
    with open(name, 'r') as file:
        text = file.read()
    sock.send(str(len(text)).encode())
    sock.send(text.encode())
    return


def recv_file(name, sock):
    length = sock.recv(1024).decode()
    text = sock.recv(int(length)).decode()
    with open(name, 'w') as file:
        file.write(text)
    return


HOST = '127.0.0.1'
PORT = 9090

sock = socket.socket()
sock.connect((HOST, PORT))
print(f"Присоединились к {HOST} {PORT}")
while True:
    request = input()
    if request == 'exit':
        break
    elif request.split()[0] == 'send':
        send_file(request.split()[1], sock)
    elif request.split()[0] == 'recv':
        recv_file(request.split()[1], sock)
    else:
        sock.send(request.encode())

    answer = sock.recv(1024).decode()
    print(answer)

sock.close()
