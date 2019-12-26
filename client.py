import socket
PORT = 12233
sock = socket.socket()
sock.connect(('localhost', PORT))
response = ''
while True:
    print('Вас приветствует мастер по логину, пожалуйста, войдите в систему.')
    login = input('Login: ')
    sock.send(login.encode())
    password = input('Password: ')
    sock.send(password.encode())
    response = sock.recv(1024)
    print(response.decode())
    if response.decode() == 'Success':
        break
    else:
        answer = input()
        sock.send(answer.encode())
        if answer == '1':
            login = input('New_Login: ')
            sock.send(login.encode())
            password = input('New_Password: ')
            sock.send(password.encode())
            break


while True:
    request = input('input: ')
    if request == "close":
        break
    sock.send(request.encode())
    response = sock.recv(1024)
    print(response.decode())

print('Спасибо за внимание')
print("Вы отключились от данного нечта")
sock.close()