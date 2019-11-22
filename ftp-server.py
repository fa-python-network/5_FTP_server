import socket
import os
import shutil
import logging
import json
import hashlib
import binascii
from threading import Thread

"""
pwd - print working directory name
ls - shows inner of working dir
cat <filename> - shows inner of file
mkdir <dir name> - make dir
remdir <dir name> - delete dir with evrthng in it
rm <filename> - delete file
rename <filename> - rename file
sends <filename1> <filename2> - send f1 to server as f2
sendc <filename1> <filename2> - send f1 to client as f2
cd <..>/<dir_name> - change dir <1 lvl down>/<1 lvl up>
"""

PORT = 1556
hom_dir = os.path.join(os.getcwd(), 'docs')
cur_dir = hom_dir

def hash_password(password: str) -> str:

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password: str, provided_password: str) -> bool:

    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def connection_with_auth(sock):

    conn, addr = sock.accept()
    address = ':'.join([str(i) for i in addr])
    if address in data_users['users']:
        conn.send(f"Hello {data_users['users'][address]['name']}! Enter passw".encode())
        while True:
            data_password = conn.recv(1024).decode()
            if not data_password:
                conn.send(f"Incorrect passw".encode())
            else:
                if verify_password(data_users['users'][address]['password'], data_password):
                    conn.send(f"Welcome".encode())
                    break
                else:
                    conn.send(f"Incorrect passw".encode())
            conn.send("Enter passw".encode())
    else:
        conn.send(f"Name:".encode())
        data_name = conn.recv(1024).decode()
        conn.send(f"Passw:".encode())
        data_pass = conn.recv(1024).decode()
        if not data_name or not data_pass:
            conn.send(f"Incorrect".encode())
            return None, None, None
        data_users['users'][address] = {'name': data_name, 'password': hash_password(data_pass)}
        with open('data_users.json', 'w') as file:
            json.dump(data_users, file)
        conn.send(f"Welcome {data_name}. Password added".encode())
    # conn.send("Ok".encode())
    return conn, addr, data_users['users'][address]['name']


class ClientThread(Thread):
    def __init__(self, conn, addr, name):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.ip = addr[0]
        self.port = addr[1]
        self.name = name

        logger.info(f"Connect client {addr[0]}:{addr[1]}")

    def run(self):

        while True:
            try:
                data = self.conn.recv(1024).decode()
                if data == 'stop' or not data:
                    logger.info(f"Disconnect client {self.addr[0]}:{self.addr[1]}")
                    self.conn.close()
                    break
                else:
                    logger.info(f"From client {self.addr[0]}:{self.addr[1]} - {data}")
                    response = self.process(data)
                    logger.info(f"To client {self.addr[0]}:{self.addr[1]} - {response}")
                    try:
                        self.conn.send(response.encode())
                    except BrokenPipeError:
                        logger.info(f"Disconnect client {self.addr[0]}:{self.addr[1]}")
                    # conn.send(data.upper())
            except ConnectionResetError:
                self.conn.close()

    def process(self, req):
        global cur_dir
        global hom_dir
        try:
            bool_var = False
            for i in ['pwd', 'ls', 'cat', 'mkdir', 'remdir', 'rm', 'rename', 'sends', 'sendc', 'cd']:
                if req.startswith(i):
                    bool_var = True
                    break
            assert bool_var, "Incorrect command"
            if req == 'pwd':
                return cur_dir

            elif req == 'ls':
                return '; '.join(os.listdir(cur_dir))

            elif req[:3] == 'cat':
                filename = req[4:]
                if filename not in os.listdir(cur_dir):
                    return "Dir doesnt exist"
                else:
                    with open(os.path.join(cur_dir, filename), 'r', encoding='utf-8') as f:
                        inner = f.read()
                        return inner

            elif req[:5] == 'mkdir':
                filename = req[6:]
                if filename in os.listdir(cur_dir):
                    return "Dir doesnt exist"
                else:
                    if filename.startswith(cur_dir):
                        os.mkdir(os.path.join(cur_dir, filename))
                        return 'Dir ' + req[6:] + ' created'
                    else:
                        return "Err"
            elif req[:6] == 'remdir':
                filename = req[7:]
                if filename not in os.listdir(cur_dir):
                    return "Dir doesnt exist"
                else:
                    shutil.rmtree(os.path.join(cur_dir, filename))
                    return 'Dir ' + req[7:] + ' deleted'

            elif req[:2] == 'rm':
                filename = req[3:]
                if filename not in os.listdir(cur_dir):
                    return "File doesnt exist"
                else:
                    os.remove(os.path.join(cur_dir, filename))
                    return 'File ' + req[3:] + ' deleted'

            elif req[:6] == 'rename':
                lst = list(req.split())
                if len(lst) != 3:
                    return "Incorrect args"
                else:
                    if lst[1] not in os.listdir(cur_dir):
                        return "File doesnt exist"
                    else:
                        os.rename(os.path.join(cur_dir, lst[1]), os.path.join(cur_dir, lst[2]))
                        return 'File ' + lst[1] + ' renamed to ' + lst[2]
            elif req[:5] == 'sends':
                lst = list(req.split(' ', 2))
                if lst[1] in os.listdir(os.path.join(os.getcwd(), 'server')):
                    return "Can't rewrite file"
                else:
                    with open(os.path.join(os.path.join(os.getcwd(), 'server'), lst[1]), 'w', encoding='utf-8') as f2:
                        f2.write(' '.join(lst[2:]))
                        return "File copied"
            elif req[:5] == 'sendc':
                lst = list(req.split())
                with open(os.path.join(os.path.join(os.getcwd(), 'server'), lst[1]), 'r', encoding='utf-8') as f1:
                    inner = f1.read()
                    string = 'sendc ' + lst[2] + ' ' + inner
                self.conn.send(string.encode())

            elif req[:2] == 'cd':
                if len(req)==2:
                    return "Err"
                elif req[3:5] == '..':
                    parts = cur_dir.split("/")
                    pathing = "/".join(parts[:-1])
                    if pathing.startswith(hom_dir):
                        os.chdir(pathing)
                    else:
                        return "Err"
                else:
                    pathing = cur_dir + '/' + req[3:]
                    if pathing.startswith(hom_dir):
                        os.chdir(pathing)
                    else:
                        return "Err"
                cur_dir = os.getcwd()
                return "Dir changed"

        except AssertionError:
            return "Incorrect command"

try:
    with open("data_users.json", "r") as read_file:
        data_users = json.load(read_file)
except FileNotFoundError:
    with open("data_users.json", 'wt') as write_file:
        data_users = {'users': {}}
        json.dump(data_users, write_file)

#  Создается и используется объект логгирования
logger = logging.getLogger("serverLogger")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("server.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# logger.info("Start client session")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))
# sock.listen(5)
# print("Listen port", PORT)
# conn, addr = sock.accept()
# logger.info(f"Connect client {addr[0]}:{addr[1]}")
threads = []
while True:
    sock.listen()
    clientsock, clientAddress, name = connection_with_auth(sock)
    newthread = ClientThread(clientsock, clientAddress, name)
    newthread.start()

conn.close()
sock.close()
