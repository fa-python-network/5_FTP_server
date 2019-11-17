import asyncio
async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 9095)
    while True:
        data = await reader.read(1000)
        if data.decode()!='this message is never going to be printed':
            print(f'SERVER: {data.decode()}')
        message = input()
        writer.write(message.encode())
        if message == 'exit':
                writer.close()
                print('Bye, client')
                break
        

asyncio.run(tcp_echo_client())