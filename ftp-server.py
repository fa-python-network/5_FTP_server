from socket import socket
from threading import Thread
import os


def main(home_dir):
    def ls(conn):
        ls_result = '\n'.join(os.listdir(home_dir))
        if not ls_result:
            ls_result = 'Директория пуста'

        send_message(ls_result)

    def mkdir(path, conn):
        if not os.path.exists(path):
            os.mkdir(path)
            send_message('Директория успешно создана')
        else:
            if not os.path.isdir(path):
                send_error('Путь уже существует и не является директорией', conn)
            else:
                send_error('Директория уже существует', conn)

    def rmdir(path, conn):
        try:
            os.rmdir(path)
        except FileNotFoundError:
            send_error(answer_patterns['not_found'], conn)
        except NotADirectoryError:
            send_error('Указанный путь не ссылается на директорию', conn)
        except BaseException:
            send_error('Неизвестная ошибка', conn)
        else:
            send_message('Директория успешно удалена')

    def rm(path, conn):
        try:
            os.remove(path)
        except FileNotFoundError:
            send_error(answer_patterns['not_found'], conn)
        except PermissionError:
            send_error('Недостаточно прав или указанный путь ссылается на директорию', conn)
        else:
            send_message('Файл успешно удалён')

    def mv(old_path, new_path, conn):
        try:
            os.rename(old_path, new_path)
        except FileNotFoundError:
            send_error(answer_patterns['not_found'], conn)
        else:
            send_message('Файл успешно переименован')

    def cp(path, conn):
        try:
            f = open(path, 'rb')
        except PermissionError:
            send_error('Недостаточно прав', conn)
        except FileNotFoundError:
            send_error(answer_patterns['not_found'], conn)
        else:
            chunk = f.read(1024)
            while chunk:
                conn.send(chunk)
                chunk = f.read(1024)
            conn.send(delimiter.encode())
            f.close()

    def push(path, conn):
        chunk = conn.recv(1024)
        if error_sign in chunk.decode():
            return

        with open(path, 'wb') as f:
            last_chunks = chunk
            while True:
                chunk = conn.recv(1024)
                last_chunks += chunk
                if last_chunks.endswith(delimiter.encode()) or not chunk:
                    f.write(last_chunks.decode()[:-len(delimiter)].encode())
                    break
                else:
                    if len(last_chunks) > 1024 * 2:
                        to_write, last_chunks = last_chunks[:1024], last_chunks[1024:]
                        f.write(to_write)
            f.close()


    def send_message(msg):
        conn.send((msg + delimiter).encode())
        print(f'"{msg}" sent to client')

    def send_error(error_msg, conn):
        conn.send(error_sign.encode())
        send_message(error_msg)


    def handle_client(conn, addr):
        while True:
            data = b''
            while True:
                try:
                    chunk = conn.recv(1024)
                except ConnectionResetError:
                    chunk = b''
                    
                data += chunk
                if data.endswith(delimiter.encode()):
                    data = data.decode()[:-len(delimiter)]
                    break
                elif not chunk:
                    data = 'exit'
                    break

            print(f'Server have got "{data}" from {addr}')

            cmd, *args = data.split()
            args.append(conn)

            if cmd != 'exit':
                commands_dict[cmd](*args)
            else:
                break

        conn.close()
        print(f'Connection with {addr} finished')

    commands_dict = {
        'ls': ls,
        'mkdir': mkdir,
        'rmdir': rmdir,
        'rm': rm,
        'mv': mv,
        'cat': cp,
        'cp': cp,
        'push': push
    }

    answer_patterns = {
        'not_found': 'Указанный путь не существует'
    }

    while True:
        conn, addr = sock.accept()
        addr = addr[0]
        print(f'New client "{addr}" connected')

        new_client_handler = Thread(target=handle_client, args=(conn, addr))
        new_client_handler.start()
        

def ensure_make_dir(dir_path, *path_parts):
    if path_parts:
        dir_path = os.path.join(dir_path, *path_parts)

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    elif not os.path.isdir(dir_path):
        os.remove(dir_path)
        os.mkdir(dir_path)

    return os.path.abspath(dir_path)


delimiter = ';;stop;;'
error_sign = ';;error;;'

sock = socket()
print('Server started here')

host, port = '', 8000
home_dir = ensure_make_dir(os.path.curdir, 'server_dir')
os.chdir(home_dir)

sock.bind((host, port))
sock.listen(5)
print('Port listening started')

main(home_dir)

sock.close()

print('Server stopped')
