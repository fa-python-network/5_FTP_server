import socket
import os
import logging
from multiprocessing import Pool

PREAMBULA=("COMMANDS:\n"
           "pwd - present working directory\n"
           "cd [path] - change directory\n"
           "ls - list of directories and files\n"
           "walk - hierarchical viewing of all directories and files\n"
           "cat [file] - concatenate a file\n"
           "mkdir [name] - create directory\n"
           "rmdir [name] - remove directory\n"
           "touch [name] - create file\n"
           "rnm [previous name] [new name] - rename file\n"
           "rm [name] - remove file\n"
           "exit - disconnect from server\n")

logging.basicConfig(filename='server.log', level=logging.INFO)
HOST = 'localhost'
PORT = 7777
start_dir = os.getcwd()  # Absolute root
relstart_dir = os.path.relpath(start_dir, start=start_dir)  # Relative root
current_dir = os.path.join(os.getcwd())  # Absolute current
relcurrent_dir = relstart_dir  # Relative current


def user_init():
    # Initializing of new user
    global NICKNAME
    global start_dir
    global relstart_dir
    global current_dir
    global relcurrent_dir
    dirname = os.path.join(current_dir, NICKNAME)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    start_dir = os.path.abspath(dirname)
    relstart_dir = os.path.relpath(start_dir, start=start_dir)
    current_dir = start_dir
    relcurrent_dir = relstart_dir


def process(req):
    global NICKNAME
    global start_dir
    global relstart_dir
    global current_dir
    global relcurrent_dir
    if req == 'pwd':
        return '/' + relcurrent_dir

    elif req[:3] == 'cd ':
        if req[:3] == 'cd ' and req[3:4] != '':
            if req[:5] == 'cd ..':
                if relcurrent_dir != relstart_dir:
                    current_dir = os.path.abspath(os.path.join(current_dir, req[3:]))
                    relcurrent_dir = os.path.relpath(os.path.join(current_dir, req[3:]), start=relstart_dir)
                    return '/' + relcurrent_dir

                else:
                    return '/' + relcurrent_dir

            else:
                if ((req[:4] == 'cd /' or req[:4] == 'cd .')
                        and req[4:] == ''):
                    current_dir = start_dir
                    relcurrent_dir = relstart_dir
                    return '/' + relcurrent_dir

                elif ((req[:4] == 'cd /' or req[:4] == 'cd .')
                      and req[4:] != ''):
                    current_dir = os.path.abspath(os.path.join(current_dir, req[4:]))
                    relcurrent_dir = os.path.relpath(os.path.join(relcurrent_dir, req[4:]), start=relstart_dir)
                    return '/' + relcurrent_dir

                else:
                    current_dir = os.path.abspath(os.path.join(current_dir, req[3:]))
                    relcurrent_dir = os.path.relpath(os.path.join(relcurrent_dir, req[3:]), start=relstart_dir)
                    return '/' + relcurrent_dir

        else:
            return 'Invalid syntax: cd [path]'

    elif req == 'ls':
        res = os.listdir(current_dir)
        if len(res) == 0:
            res = '..'
        return '\n'.join(res)

    elif req == 'walk':
        directories = ''
        files = ''
        for dirpath, dirnames, filenames in os.walk(relcurrent_dir):
            for dirname in dirnames:
                directories += 'Directory:%s' % os.path.join(dirpath, dirname) + '\n'
            for filename in filenames:
                files += 'File:%s' % os.path.join(dirpath, filename) + '\n'
        walk = directories + files
        return walk

    elif req[:4] == 'cat ':
        filename = req[4:]
        filename = os.path.join(current_dir, filename)
        try:
            f = open(filename, 'rt')
            res = f.read()
            f.close()
            if res == '':
                return 'File is empty'
            return res

        except FileNotFoundError:
            return 'File not found'

    elif req[:6] == 'mkdir ':
        name = req[6:]
        dirname = os.path.join(current_dir, name)
        try:
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
                message = "Created %s" % name
                return message

            else:
                return 'Directory already exist'

        except:
            return 'Unable to create directory'

    elif req[:6] == 'rmdir ':
        name = req[6:]
        dirname = os.path.join(current_dir, name)
        try:
            if os.path.isdir(dirname):
                os.rmdir(dirname)
                message = "Removed %s" % name
                return message

            else:
                return '%s is not a directory' % name

        except:
            return 'Unable to remove directory'

    elif req[:6] == 'touch ':
        name = req[6:]
        filename = os.path.join(current_dir, name)
        try:
            if not os.path.isfile(filename):
                open(filename, 'tw')
                message = "Created %s" % name
                return message

            else:
                return 'File already exist' \
                       ''
        except:
            return 'Unable to create file'

    elif req[:4] == 'rnm ':
        splited = req.split(' ')
        if len(splited) == 3:
            lastname = os.path.join(current_dir, splited[1])
            newname = os.path.join(current_dir, splited[2])
            try:
                if os.path.isfile(lastname):
                    os.rename(lastname, newname)
                    message = '%s renamed to %s' % (splited[1], splited[2])
                    return message

                else:
                    message = '%s is not a file' % splited[1]
                    return message

            except:
                'Unable to rename file'

        else:
            return 'Syntax error: rnm [last name] [new name]'
        return str(splited)

    elif req[:3] == 'rm ':
        name = req[3:]
        filename = os.path.join(current_dir, name)
        try:
            if os.path.isfile(filename):
                os.remove(filename)
                message = "Removed %s" % name
                return message

            else:
                return '%s is not a file' % name

        except:
            return 'Unable to remove file'

    elif req == 'exit':
        return 'exit'

    elif req[:6] == 'snd:::':
        splited = req.split(':::')
        name = splited[1]
        filename = os.path.join(current_dir, name)
        res = splited[2]
        try:
            if not os.path.isfile(filename):
                f = open(filename, 'tw')
                f.write(res)
                message = "Created %s" % name
                return message

            else:
                return 'File already exist'

        except:
            return 'Unable to create file'

    elif req[:5] == 'recv ':
        filename_user = req[5:]
        filename = os.path.join(current_dir, filename_user)
        try:
            if os.path.isfile(filename):
                f = open(filename, 'r', encoding='utf-8')
                res = f.read()
                f.close()
                req = 'recv:::%s:::%s' % (filename_user, res)
                return req

            else:
                return '%s is not a file' % filename

        except:
            return 'Unable to read file'

    return 'Bad request'


def auth(request):
    global AUTH
    global NICKNAME
    splited = request.split(':::')
    client_nick = splited[0]
    NICKNAME = client_nick
    client_passwd = splited[1]
    logpass = client_nick + ':' + client_passwd
    res = splited[2]
    f = open('whitelist.txt', 'r')
    for row in f.readlines():
        if row.rstrip() == logpass:
            AUTH = True
            return res

    else:
        return False


def send_interface(data):
    print('Server:', data)
    conn.send(data.encode())
    conn.close()


def client_pool(conn, addr):
    pass


if __name__ == '__main__':
    sock = socket.socket()
    sock.bind((HOST, PORT))
    print("Listening port", PORT)
    pool = Pool()
    while True:
        NICKNAME = ''
        current_dir = '.'
        AUTH = False
        INIT = False
        sock.listen(0)
        conn, addr = sock.accept()
        log = 'Connection from %s:%s' % (addr[0], addr[1])
        print(log)
        try:
            while True:
                data = conn.recv(1024).decode('utf-8', 'ignore')
                if not data:
                    break
                print('Client:', data)
                request = auth(data)
                if request:
                    if not INIT:
                        user_init()
                        INIT = True
                        send_interface(PREAMBULA)
                    response = process(request)
                    if response == 'exit':
                        exit_message = 'Disconnected from server'
                        send_interface(response)
                        break
                    print('Server:', response)
                    conn.send(response.encode())

                else:
                    exit_message = 'Invalid user'
                    send_interface(exit_message)
                    break

        except Exception as ex:
            print('No calls received from client %s:%s, ex: %s' % (addr[0], addr[1], ex))
        log = 'Client %s:%s disconnected' % (addr[0], addr[1])
        print(log)
        print('===')
        conn.close()
