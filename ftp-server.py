from socket import socket
from threading import Thread
import os


def main(SWD):
    def ls(conn):
        dir_list = '\n'.join(os.listdir(SWD))
        if not dir_list:
            dir_list = 'Рабочая директория пуста'

        send_message(dir_list)

    def mkdir(path, conn):
        if not os.path.exists(path):
            os.mkdir(path)
            send_message('Директория успешно создана')
        else:
            if not os.path.isdir(path):
                send_error('Указанный путь уже существует и это не директория', conn)
            else:
                send_error('Директория уже существует', conn)

    def rmdir(path, conn):
        try:
            os.rmdir(path)
        except FileNotFoundError:
            send_error(answers['not_found'], conn)
        except NotADirectoryError:
            send_error('Указанный путь ссылается не на директорию', conn)
        except BaseException:
            send_error('Неизвестная ошибка', conn)
        else:
            send_message('Директория успешно удалена')

    def rm(path, conn):
        try:
            os.remove(path)
        except FileNotFoundError:
            send_error(answers['not_found'], conn)
        except PermissionError:
            send_error('Недостаточно прав или путь ссылается на директорию', conn)
        else:
            send_message('Файл успешно удалён')

    def mv(old_path, new_path, conn):
        try:
            os.rename(old_path, new_path)
        except FileNotFoundError:
            send_error(answers['not_found'], conn)
        else:
            send_message('Файл успешно переименован')

    def pull(path, conn):
        try:
            f = open(path, 'rb')
        except PermissionError:
            send_error('Недостаточно прав', conn)
        except FileNotFoundError:
            send_error(answers['not_found'], conn)
        else:
            chunk = f.read(1024)
            while chunk:
                conn.send(chunk)
                chunk = f.read(1024)
            conn.send(DEL.encode())
            f.close()

    def push(path, conn):
        chunk = conn.recv(1024)
        if err_disclaimer in chunk.decode():
            return

        with open(path, 'wb') as f:
            last_chunks = chunk
            while True:
                chunk = conn.recv(1024)
                last_chunks += chunk
                if last_chunks.endswith(DEL.encode()) or not chunk:
                    # декодировать нужно, чтобы делать срез именно по символам, а не по байтам
                    f.write(last_chunks.decode()[:-len(DEL)].encode())
                    break
                else:
                    if len(last_chunks) > 1024 * 2:
                        to_write, last_chunks = last_chunks[:1024], last_chunks[1024:]
                        f.write(to_write)
            f.close()


    def send_message(msg):
        conn.send((msg + DEL).encode())

    def send_error(err, conn):
        conn.send(err_disclaimer.encode())
        send_message(err)
        print(f'{err} sent to client')

    def new_client(conn, addr):
        while True:
            command = ''
            while True:
                try:
                    chunk = conn.recv(1024)
                except ConnectionResetError:
                    chunk = b''

                command += chunk.decode()
                if command.endswith(DEL):
                    command = command[:-len(DEL)]
                    break
                elif not chunk:
                    command = 'exit'
                    break

            print(f'Server received "{command}" from {addr}')

            cmd_name, *args = command.split()
            args.append(conn)

            if cmd_name != 'exit':
                commands_dict[cmd_name](*args)
            else:
                break

        conn.close()
        print(f'{addr} disconnected')

    commands_dict = {
        'ls': ls,
        'mkdir': mkdir,
        'rmdir': rmdir,
        'rm': rm,
        'mv': mv,
        'cat': pull,
        'pull': pull,
        'push': push
    }

    answers = {
        'not_found': 'Указанный путь не существует'
    }

    while True:
        conn, addr = sock.accept()
        addr = addr[0]
        print(f'Connected to "{addr}"')

        Thread(target=new_client, args=(conn, addr)).start()


SWD = os.path.abspath(os.path.join(os.path.curdir, 'server_work_directory'))
if not os.path.exists(SWD):
    os.mkdir(SWD)
elif not os.path.isdir(SWD):
    os.remove(SWD)
    os.mkdir(SWD)
os.chdir(SWD)

DEL = 'ВСЁ_СТОП_ЭТО_КОНЕЦ'
err_disclaimer = 'ПРОИЗОШЛА_ОШИБОЧКА'

with socket() as sock:
    sock.bind(('', 8888))
    print('Server started here')

    sock.listen(8)
    print('Port listening started')

    main(SWD)

print('"main" finished')
