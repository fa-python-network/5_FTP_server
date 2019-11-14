import socket
PORT = 12345
sock = socket.socket()
sock.connect(('localhost', PORT))
response = ''
k = 0
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
    with open("commands.txt") as file:
        f = file.read()
    comm = f.split('\n')
    for i in range(len(comm)):
        request = comm[i]
        if request == "close":
            break
        sock.send(request.encode())
        response = sock.recv(1024)
        print(response.decode())
        k += 1
        print(k)
    if k == 10:
        print("ЩЩЩКАААРНО, всё работает в норме!")
        break

print('Bыполнил Никитин Роман выполнил Никитин Роман')
proverka = input('Закрыть клиент и сервер? y/n')
if proverka == 'y':
    print("closed")
    sock.close()
sock.recv(1)