import asyncio
import sys
import os
import colorama
import re
import shutil


def list_files(addr_ip: str) -> str:
    message_new = ''
    startpath = addr_ip

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        message_new += f'\n{colorama.Fore.CYAN}{indent}{os.path.basename(root)}/'
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            message_new += f'\n{subindent}{f}'

    message_new += colorama.Style.RESET_ALL
    return message_new


def terminal_warning(warning: str) -> None:
    print(f'{colorama.Fore.CYAN}{warning}{colorama.Style.RESET_ALL}')


def create_private_directory(addr_ip: str) -> None:
    if addr_ip not in [i for i in os.listdir() if not os.path.isfile(i)]:
        os.mkdir(addr_ip)
        terminal_warning(f'Created a private directory for {addr_ip}')
    else:
        terminal_warning(f'{addr_ip} already have their private directory')


def create_directory(addr_ip: str, directory_name: str) -> None:
    if directory_name not in [i for i in os.listdir(addr_ip) if not os.path.isfile(i)]:
        os.mkdir(f'{addr_ip}/{directory_name}')
        terminal_warning(f'Created directory {directory_name!r} for {addr_ip}')
    else:
        terminal_warning(f'{addr_ip} already have directory {directory_name!r}')


def delete_directory(addr_ip: str, directory_name: str) -> None:
    if directory_name in [i for i in os.listdir(addr_ip) if not os.path.isfile(i)]:
        shutil.rmtree(f'{addr_ip}/{directory_name}')
        terminal_warning(f'Removed {directory_name!r} for {addr_ip}')
    else:
        terminal_warning(f'{addr_ip} don\'t have {directory_name!r}')


def delete_file(addr_ip: str, file_name: str) -> None:
    if os.path.exists(f'{addr_ip}/{file_name}'):
        os.remove(f'{addr_ip}/{file_name}')
        terminal_warning(f'Removed {file_name!r} for {addr_ip}')
    else:
        terminal_warning(f'{addr_ip} don\'t have {file_name!r}')


def rename_file(addr_ip: str, file_name: str, new_file_name: str) -> None:
    if os.path.exists(f'{addr_ip}/{file_name}'):
        os.rename(f'{addr_ip}/{file_name}', f'{addr_ip}/{new_file_name}')
        terminal_warning(f'Removed {file_name!r} for {addr_ip}')
    else:
        terminal_warning(f'{addr_ip} don\'t have {file_name!r}')


async def receive_file(reader, addr_ip: str, file_name: str) -> None:
    data = await reader.read(1024)
    payload_size = int.from_bytes(data, 'big')

    with open(f'{addr_ip}/{file_name}', 'wb') as f:
        data = await reader.read(payload_size)
        f.write(data)


async def send_file(writer, addr_ip: str, file_name: str) -> None:
    if os.path.exists(f'{addr_ip}/{file_name}'):
        payload_size = os.path.getsize(f'{addr_ip}/{file_name}')

        writer.write(payload_size.to_bytes(1024, 'big'))
        await writer.drain()

        with open(f'{addr_ip}/{file_name}', 'rb') as f:
            data = f.read(payload_size)
        
            writer.write(data)
            await writer.drain()


async def handle(reader, writer) -> None:
    addr = writer.get_extra_info('peername')
    addr_ip: str = addr[0]

    # create the user's private directory
    create_private_directory(addr_ip)

    # welcome!
    message_new = f'You\'re welcome, {addr_ip}!'
    writer.write(message_new.encode())
    await writer.drain()
    print(f'{addr!r} << {message_new!r}')

    while True:
        data = await reader.read(100)
        message = data.decode()
        print(f'{addr!r} >> {message!r}')

        if message == 'exit':
            writer.close()
            terminal_warning(f'{addr_ip} DISCONNECTED!')
            break
        elif message == 'ls':
            message_new = list_files(addr_ip)
            writer.write(message_new.encode())
            await writer.drain()

            terminal_warning(f'{addr_ip} look up the contents of their private directory')
            continue
        elif re.match(r'^mkdir (?P<path>[\w\-. ]+)$', message):
            directory_name: str = re.match(r'^mkdir (?P<path>[\w\-. ]+)$', message).group('path')
            create_directory(addr_ip, directory_name)
            message_new = f'Done!'
        elif re.match(r'^rmdir (?P<path>[\w\-. ]+)$', message):
            directory_name: str = re.match(r'^rmdir (?P<path>[\w\-. ]+)$', message).group('path')
            delete_directory(addr_ip, directory_name)
            message_new = f'Done!'
        elif re.match(r'^rmfile (?P<path>[\w\-. /]+)$', message):
            file_name: str = re.match(r'^rmfile (?P<path>[\w\-. /]+)$', message).group('path')
            delete_file(addr_ip, file_name)
            message_new = f'Done!'
        elif re.match(r'^refile (?P<path>[\w\-. /]+) (?P<path_new>[\w\-. /]+)$', message):
            mtch = re.match(r'^refile (?P<path>[\w\-. /]+) (?P<path_new>[\w\-. /]+)$', message)
            file_name: str = mtch.group('path')
            new_file_name: str = mtch.group('path_new')
            rename_file(addr_ip, file_name, new_file_name)
            message_new = f'Done!'
        elif re.match(r'^download (?P<path>[\w\-. /]+)$', message):
            file_name: str = re.match(r'^download (?P<path>[\w\-. /]+)$', message).group('path')
            await send_file(writer, addr_ip, file_name)
            message_new = f'Done!'
        elif re.match(r'^upload (?P<path>[\w\-. /]+)$', message):
            file_name: str = re.match(r'^upload (?P<path>[\w\-. /]+)$', message).group('path')
            await receive_file(reader, addr_ip, file_name)
            message_new = f'Done!'
        else:
            message_new = 'Use a command, please'

        writer.write(message_new.encode())
        await writer.drain()
        print(f'{addr!r} << {message_new!r}')


async def main() -> None:
    server = await asyncio.start_server(
        handle, '127.0.0.1', 9095)

    addr = server.sockets[0].getsockname()
    terminal_warning(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
