import asyncio
import sys
import os
import colorama
import re


async def receive_file(reader, file_name: str) -> None:
    data = await reader.read(1024)
    payload_size = int.from_bytes(data, 'big')

    if '/' in file_name:
        file_name = file_name.split('/')[-1]

    with open(file_name, 'wb') as f:
        data = await reader.read(payload_size)
        f.write(data)


async def send_file(writer, file_name: str) -> None:
    if os.path.exists(f'{file_name}'):
        payload_size = os.path.getsize(f'{file_name}')

        writer.write(payload_size.to_bytes(1024, 'big'))
        await writer.drain()

        with open(f'{file_name}', 'rb') as f:
            data = f.read(payload_size)
        
            writer.write(data)
            await writer.drain()


async def tcp_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 9095)

    data = await reader.read(100)
    print(f'SERVER: {data.decode()!r}')

    while True:
        message = input('> ')
        writer.write(message.encode())
        await writer.drain()

        if message == 'exit':
            writer.close()
            print('Bye, client')
            break
        elif message == 'ls':
            data = await reader.read(1024)
            print(f'SERVER: {data.decode()}')
            continue
        elif re.match(r'^download (?P<path>[\w\-. /]+)$', message):
            file_name: str = re.match(r'^download (?P<path>[\w\-. /]+)$', message).group('path')
            await receive_file(reader, file_name)
        elif re.match(r'^upload (?P<path>[\w\-. /]+)$', message):
            file_name: str = re.match(r'^upload (?P<path>[\w\-. /]+)$', message).group('path')
            await send_file(writer, file_name)

        data = await reader.read(100)
        print(f'SERVER: {data.decode()!r}')


if __name__ == '__main__':
    print("""
    Commands:
    - exit - bb
    - ls - show my private directory as a tree
    - mkdir %PATH% - create a directory
    - rmdir %PATH% - remove a directory
    - rmfile %PATH% - remove a file
    - refile %PATH% - rename a file
    - download %PATH% - download a file
    - upload %PATH% - upload a file
    """)
    
    asyncio.run(tcp_client())