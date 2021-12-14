import socket
import os
import config
import shutil

dirname = os.path.join(os.getcwd(), 'docs')


def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif 'cat' in req.split():
        return cat(req.split(' ')[1])
    elif 'mkdir' in req.split():
        return mkdir(req)
    elif 'rmdir' in req.split():
        return rmdir(req)
    elif 'rmfile' in req.split():
        return rmfile(req)
    elif 'mv' in req.split():
        return mv(req)
    elif 'touch' in req.split():
        return touch(req)
    elif req == 'help':
        return config.HELP
    return 'bad request'


def cat(filename):
    with open(os.path.join(dirname, filename), 'r') as f:
        return ''.join(f.readlines())


def touch(req):
    if len(req.split()) == 2:
        filename, text = req.split()[1], ''
    else:
        filename, text = req.split()[1], ' '.join(req.split()[2:])
    try:
        with open(os.path.join(dirname, filename), 'w') as f:
            f.write(text)
        return f"File '{filename}' created"
    except Exception as e:
        return f"File '{filename}' not created: {e}"


def mv(req):
    source, destination = req.split()[1:3]
    try:
        os.rename(os.path.join(dirname, source), os.path.join(dirname, destination))
        return f"'{source}' changed to '{destination}'"
    except Exception as e:
        return f"not renamed: {e}"


def rmdir(req):
    dir = req.split()[1]
    try:
        shutil.rmtree(os.path.join(dirname, dir))
        return f"Directory '{dir}' removed"
    except Exception as e:
        return f"'dir' not removed: {e}"


def rmfile(req):
    filename = req.split()[1]
    try:
        os.remove(os.path.join(dirname, filename))
        return f"File '{filename}' deleted"
    except Exception as e:
        return f"File '{filename}' not deleted"


def mkdir(req):
    try:
        new_dir = req.split()[1]
        os.mkdir(os.path.join(dirname, new_dir))
        return f"Created directory '{new_dir}'"
    except FileExistsError as e:
        return f"'{new_dir}' already exists"


sock = socket.socket()
sock.bind(('', config.PORT))
sock.listen()
print("Прослушиваем порт", config.PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    if request == 'exit':
        conn.send(config.INTERRUPT_MESSAGE.encode())
        break
    if request.split()[0] == 'getfile':
        filename = request.split()[1]
        bytes_read = ' '.join(request.split()[2:]).encode()
        try:
            with open(os.path.join('docs', 'server', filename), 'wb') as f:
                while True:
                    print(bytes_read)
                    f.write(bytes_read)
                    if len(bytes_read) < 1024:
                        break
                    bytes_read = conn.recv(1024)
            conn.send(f"File '{filename}' received".encode())
        except Exception as e:
            conn.send(f"File '{filename}' transfer error: {e}".encode())
    elif request.split()[0] == 'sendfile':
        filename = request.split()[1]
        try:
            with open(os.path.join('docs', 'server', filename), 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    conn.send(bytes_read)
            conn.send(f"File '{filename}' sent".encode())
        except Exception as e:
            conn.send(f"File '{filename}' transfer error: {e}".encode())
    else:
        response = process(request)
        conn.send(response.encode())
conn.close()
