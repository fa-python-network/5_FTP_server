import socket
PORT = 12345
sock = socket.socket()
sock.connect(('localhost', PORT))
response = ''
while True:
    print('Bыполнил Никитин Роман выполнил Никитин Роман')
    login = input('Login')
    sock.send(login.encode())
    password = input('Password')
    sock.send(password.encode())
    response = sock.recv(1024)
    print(response.decode())
    if response.decode() == 'Success':
        break
    else:
        answer = input()
        sock.send(answer.encode())
        if answer == '1':
            login = input('NEW_Login')
            sock.send(login.encode())
            password = input('NEW_Password')
            sock.send(password.encode())
            break


while True:
    request = input('che?')
    if request == "close":
        break
    sock.send(request.encode())
    response = sock.recv(1024)
    print(response.decode())

print('Bыполнил Никитин Роман выполнил Никитин Роман')
print("closed")
sock.close()
