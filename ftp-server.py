import socket
import os

"""
pwd
ls
cat <filename>

"""
PORT = 8888
curr_dir = os.path.join(os.getcwd(), 'docs')
cur_dir = os.getcwd()
os.chdir('docs')
def process(req):
    global curr_dir
    if req == 'pwd':
        return curr_dir

    elif req == 'ls':
        return '; '.join(os.listdir(curr_dir))

    elif req[:6] == "mkdir ":
        os.mkdir(req[6:])
        return f'You created directory "{req[6:]}"'

    elif req[:6] == "rmdir ":
        os.rmdir(req[6:])
        return f'You deleted directory "{req[6:]}"'

    elif req[:3] == "cd ":
        curr_dir = os.path.join(os.getcwd(), req[3:])
        os.chdir(req[3:])
        return("You are in " + req[3:])

    elif req[:4] == "cat ":
        filename = req[4:]
        try:
            File = open(filename)
            content = File.read()
            File.close()
            return content
        except FileNotFoundError:
            return "File doesn't exist"

    elif req[:5] == "echo ":
        try:
            if len(req.split(' >> ')) == 2:
                new_st = req.split(' >> ')
                new_st[1] = os.path.join(curr_dir, new_st[1])
                file = open(new_st[1], 'a')
                file.write('\n')
                file.write(new_st[0])
                file.close()
                return f'added to {new_st[1]}'

            elif len(req.split(' > ')) == 2:
                new_st = req.split(' > ')
                new_st[1] = os.path.join(curr_dir, new_st[1])
                file = open(new_st[1], 'w')
                file.write('\n')
                file.write(new_st[0])
                file.close()
                return f'written in {new_st[1]}'
            else:
                return 'wrong format'
        except FileNotFoundError:
            return 'wrong format'
    else:
        return 'wrong command'

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(5)

while True:
    print("Listening", PORT)

    conn, addr = sock.accept()


    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())
    conn.close()
