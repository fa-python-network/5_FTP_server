import socket
import os

HOST = 'localhost'
PORT = 7777
current_dir = './'
NICKNAME = input('Nickname: ')
PASSWORD = input('Password: ')


def auth(request):
    global NICKNAME
    global PASSWORD
    request = '%s:::%s:::%s' % (NICKNAME, PASSWORD, request)
    return request


def recv_file(response):
    splited = response.split(':::')
    filename = splited[1]
    filename = os.path.join(current_dir, filename)
    res = splited[2]
    try:
        if not os.path.isfile(filename):
            f = open(filename, 'tw')
            f.write(res)
            message = 'Created %s' % filename
            return message
        else:
            return 'File already exist'
    except:
        return 'Unable to create file'


def send_file(request):
    filename_user = request[4:]
    filename = os.path.join(current_dir, filename_user)
    if os.path.isfile(filename):
        f = open(filename, 'r', encoding='utf-8')
        res = f.read()
        f.close()
        request = 'snd:::%s:::%s' % (filename_user, res)
        return request
    else:
        print('%s is not a file' % filename)


def message_handler():
    request = input('>')
    if request[:4] == 'snd ':
        request = send_file(request)
    elif request == 'exit':
        return False
    elif request == '':
        request = ' '
    return request


sock = socket.socket()
sock.connect((HOST, PORT))
while True:
    request = message_handler()
    if request:
        request = auth(request)
        sock.send(request.encode())
        response = sock.recv(1024).decode()
        if response[:7] == 'recv:::':
            response = recv_file(response)
    else:
        sock.close()
        print('Disconnected from server')
        break
    print(response)

