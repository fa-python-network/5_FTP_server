import socket
import os
import threading
def increment_client_port(number_port):
    return 1024 if number_port >= 65500 else number_port + 1

def check_input_host(host_address):
    try:
        if host_address == 'localhost':
            return True
        else:
            host_address_list = host_address.split('.')
            for i in host_address_list:
                if int(i) <= 0 or int(i) > 255:
                    return False
            else:
                return True
    except ValueError:
        return False


def check_input_port(port_number, default_value=1556):
    try:
        port_number = int(port_number)
        if 1024 > port_number or port_number >= 65535:
            raise ValueError
        print(f"Data is correct. Port is {port_number}")
    except ValueError:
        print(f"Data is not correct. Port is {default_value}")
        port_number = default_value
    return port_number


if __name__ == "__main__":
    HOST = input("Input host address IPv4 or localhost, DEFAULT - 127.0.0.1: ")

    if check_input_host(HOST):
        print(f"Data is correct. Host is {HOST}")
    else:
        print('Data is not correct. Host is 127.0.0.1')
        HOST = '127.0.0.1'

    PORT = input('Input port. Default - 1556: ')
    PORT = check_input_port(PORT)

    client_port = input('Input port of your connection. Default: 60272. ')
    client_port = check_input_port(client_port, default_value=60272)
    while True:
        try:
            sock = socket.socket()
            sock.bind(('127.0.0.1', client_port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((HOST, PORT))
            break
        except OSError:
            sock.close()
            client_port = increment_client_port(client_port)

    while True:
        resp = sock.recv(1024).decode()
        print(resp)
        if resp.startswith("Welcome"):
            break
        req = input()
        sock.send(req.encode())

    request = input(">> ")
    if not request:
        request = input(">> ")
    elif request == "stop":
        sock.send(request.encode())


    while True:
        if not request:
            request = input(">> ")
        elif request == "stop":
            sock.send(request.encode())
            break
        else:
            if request.startswith('sends'):
                lst = list(request.split())
                if len(lst) != 3:
                    print("Incorrect args")
                try:
                    with open(os.path.join(os.path.join(os.getcwd(), 'client'), lst[1]), 'r', encoding='utf-8') as f1:
                        inner = f1.read()
                        string = 'sends ' + lst[2] +' '+ inner
                    sock.send(string.encode())
                except BrokenPipeError:
                    pass
            elif request.startswith('sendc'):
                lst = list(request.split())
                if len(lst) != 3:
                    print("ncorrect args")
                else:
                    if lst[2] in os.listdir(os.path.join(os.getcwd(), 'client')):
                        print("Cant rewrite file")
                    else:
                        sock.send(request.encode())
            else:
                sock.send(request.encode())
            response = sock.recv(1024)
            if response.decode().startswith('sendc'):
                lst = list(response.decode().split(' ', 2))
                try:
                    with open(os.path.join(os.path.join(os.getcwd(), 'client'), lst[1]), 'w', encoding='utf-8') as f2:
                        f2.write(' '.join(lst[2:]))
                except BrokenPipeError:
                    pass
            else:
                print(response.decode())
            request = input(">> ")
    print('Closed')
    sock.close()