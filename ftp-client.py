from socket import socket


def send_message(msg):
    try:
        sock.send((msg + DEL).encode())
    except ConnectionError:
        print('Error while sending data')
    else:
        print('Message sent')


def receive_answer(filename=None, only_print=False):
    def receive_to_the_rest(chunk, error=False):
        if error or not only_print:
            answer = chunk.decode()[len(err_disclaimer) if error else 0:]
            while True:
                if answer.endswith(DEL):
                    return answer[:-len(DEL)]
                elif not chunk:
                    return answer

                chunk = sock.recv(1024)
                answer += chunk.decode()

        else:
            last_chunks = chunk
            while True:
                chunk = sock.recv(1024)
                last_chunks += chunk
                if last_chunks.endswith(DEL.encode()) or not chunk:
                    print(last_chunks.decode()[:-len(DEL)])
                    break
                else:
                    if len(last_chunks) > 1024 * 2:
                        to_print, last_chunks = last_chunks[:1024], last_chunks[1024:]
                        print(to_print.decode())

    chunk = sock.recv(1024)
    err = err_disclaimer in chunk.decode()
    if err or filename is None:
        return receive_to_the_rest(chunk, error=err)

    try:
        f = open(filename, 'wb')
    except BaseException:
        return 'Ошибка при создании файла'
    else:
        last_chunks = chunk
        while True:
            chunk = sock.recv(1024)
            last_chunks += chunk
            if last_chunks.endswith(DEL.encode()) or not chunk:
                # декодировать нужно, чтобы делать срез именно по символам, а не по байтам
                f.write(last_chunks.decode()[:-len(DEL)].encode())
                break
            else:
                if len(last_chunks) > 1024 * 2:
                    to_write, last_chunks = last_chunks[:1024], last_chunks[1024:]
                    f.write(to_write)
        return success_status


def pull(cmd_name, args):
    send_message(' '.join([cmd_name, args[0]]))
    answer_status = receive_answer(filename=args[1])
    if answer_status == success_status:
        print('Файл успешно обновлён')
    else:
        print(answer_status)


def push(cmd_name, args):
    send_message(' '.join([cmd_name, args[1]]))
    try:
        f = open(args[0], 'rb')
    except BaseException:
        print('Ошибка при открытии файла')
        send_message(err_disclaimer)
    else:
        chunk = f.read(1024)
        while chunk:
            sock.send(chunk)
            chunk = f.read(1024)
        sock.send(DEL.encode())
        print('Файл успешно отправлен')


def cat(cmd_name, args):
    send_message(' '.join([cmd_name, *args]))
    receive_answer(only_print=True)


def default_command(cmd_name, args):
    send_message(' '.join([cmd_name, *args]))
    answer = receive_answer()
    print(f'Received from server:\n{answer}')


DEL = 'ВСЁ_СТОП_ЭТО_КОНЕЦ'
err_disclaimer = 'ПРОИЗОШЛА_ОШИБОЧКА'
success_status = 'ЭТО_УСПЕХ'

sock = socket()

try:
    sock.connect(('localhost', 8888))
except ConnectionError:
    print("Server is not available")
else:
    print("Connected to server")

    commands = ['ls', 'mkdir', 'rmdir', 'rm', 'mv', 'cat', 'pull', 'push', 'exit']
    args_len = {
        'ls': 0,
        'mkdir': 1,
        'rmdir': 1,
        'rm': 1,
        'mv': 2,
        'cat': 1,
        'pull': 2,
        'push': 2,
        'exit': 0
    }

    complex_commands = {
        'pull': pull,
        'push': push,
        'cat': cat
    }

    while True:
        cmd_msg = input('\nВведите команду: ')
        if not cmd_msg:
            continue

        command, *args = cmd_msg.split()
        if command not in commands:
            print('Неверная команда')
            continue

        if args_len[command] != len(args):
            print(f'Ожидаемое кол-во аргументов: {args_len[command]}. Получено: {len(args)}')
            continue

        if command in complex_commands:
            complex_commands[command](command, args)
        elif command == 'exit':
            break
        else:
            default_command(command, args)


sock.close()
input('Press Enter to exit...')
