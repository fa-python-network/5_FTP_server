from socket import socket
'''
'ls' - показать содержимое рабочей директории сервера
'mkdir' - создать папку
'rmdir' - удалить папку
'rm' - удалить файл
'mv' - переименовать файл
'cat' - показать содержимое файла
'cp file1 file2' - скопировать file1 с сервера и сохранить как file2 
'push file1 file2' - залить file1 на сервер и сохранить как file2 
'exit' - выход
'''


def send_message(msg):
    try:
        sock.send((msg + delimiter).encode())
    except ConnectionError:
        print('Ошибка при отправке сообщения')
    else:
        print(f'"{msg}" отправлено на сервер {host}:{port}')


def receive_answer(print_only=False, answer_fragment=None):
    chunk = answer_fragment if answer_fragment else sock.recv(1024)
    error = error_sign in chunk.decode()

    if not print_only or error:
        answer = chunk.decode()[len(error_sign) if error else 0:]
        while True:
            if answer.endswith(delimiter):
                return answer[:-len(delimiter)]
            elif not chunk:
                return answer

            chunk = sock.recv(1024)
            answer += chunk.decode()

    else:
        last_chunks = chunk
        print(last_chunks)
        while True:
            chunk = sock.recv(1024)
            last_chunks += chunk
            if last_chunks.endswith(delimiter.encode()) or not chunk:
                print(last_chunks.decode()[:-len(delimiter)])
                break
            else:
                if len(last_chunks) > 1024 * 2:
                    checked, last_chunks = last_chunks[:1024], last_chunks[1024:]
                    print(checked.decode())
        return success_st


def receive_file(path):
    chunk = sock.recv(1024)
    if error_sign in chunk.decode():
        return receive_answer(answer_fragment=chunk)

    with open(path, 'wb') as f:
        last_chunks = chunk
        while True:
            chunk = sock.recv(1024)
            last_chunks += chunk
            if last_chunks.endswith(delimiter.encode()) or not chunk:
                f.write(last_chunks.decode()[:-len(delimiter)].encode())
                break
            else:
                if len(last_chunks) > 1024 * 2:
                    checked, last_chunks = last_chunks[:1024], last_chunks[1024:]
                    f.write(checked)
        return success_st


def cp(cmd, args):
    send_message(cmd + ' ' + args[0])
    answer_status = receive_file(args[1])
    if answer_status == success_st:
        print(f'Файл {args[0]} успешно скопирован с сервера')
    else:
        print(answer_status)


def push(cmd, args):
    try:
        f = open(args[0], 'rb')
    except FileNotFoundError:
        print('Указанный путь не существует')
    else:
        send_message(cmd + ' ' + args[1])

        chunk = f.read(1024)
        while chunk:
            sock.send(chunk)
            chunk = f.read(1024)
        sock.send(delimiter.encode())
        print('Файл успешно отправлен')


def cat(cmd, args):
    send_message(cmd + ' ' + args[0])
    answer = receive_answer(print_only=True)
    if answer != success_st:
        print(answer)


def simple_command(cmd, args):
    send_message(' '.join([cmd, *args]))
    answer = receive_answer()

    print(f'Returned by server:\n{answer}')


delimiter = ';;stop;;'
error_sign = ';;error;;'
success_st = ';;success;;'

sock = socket()
host, port = 'localhost', 8000
connected = False

try:
    sock.connect((host, port))
    connected = True
except ConnectionError:
    print("Unreachable server")

if connected:
    print(f"Connected to {host}:{port}")

    available_commands = ['ls', 'mkdir', 'rmdir', 'rm', 'mv', 'cat', 'cp', 'push', 'exit']
    special_commands = {
        'cp': cp,
        'push': push,
        'cat': cat
    }

    args_count = {
        'ls': 0,
        'mkdir': 1,
        'rmdir': 1,
        'rm': 1,
        'mv': 2,
        'cat': 1,
        'cp': 2,
        'push': 2,
        'exit': 0
    }

    while True:
        raw_cmd = input('\nВведите команду: ')
        if not raw_cmd:
            continue

        command, *args = raw_cmd.split()
        if command not in available_commands:
            print('Некорректная команда')
            continue

        if args_count[command] != len(args):
            print(f'Неверное кол-во аргументов. Ожидалось: {args_count[command]}. Получено: {len(args)}')
            continue

        if command in special_commands:
            special_commands[command](command, args)
        elif command == 'exit':
            break
        else:
            simple_command(command, args)


sock.close()

input('Press Enter to exit...')
