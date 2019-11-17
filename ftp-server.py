import asyncio
import os
import shutil

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    name=''
    check=False
    names = open('names.txt','r')
    nameflag=0#user is unknown
    for i in names:#check ip in names.txt
        
        if i.split(',')[0][2:-1]==addr[0]:#if ip is known
            nameflag=1#user is known
            
            writer.write('Hello, {0}. Enter password'.format(i.split(',')[1][2:-1]).encode())
            await writer.drain()
            
            name=i.split(',')[1][2:-1]
            while check!=True:
                psw = await reader.read(100)
                if i.split(',')[2][2:-3]==(str(psw)[2:-1]):
                    writer.write('''Welcome to my server!
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat - отправляет содержимое файла,ввод имени файла после команды
mkdir - создает папку,ввод имени файла после команды
rmdir - удаляет пустую папку,ввод имени файла после команды
remove - удаляет файл,ввод имени файла после команды
rename - переименовывает,ввод имени файла после команды
copyto - копирует txt файл на сервер, ввод имени файла после команды
copyfrom - копирует txt файл с сервера, ввод имени файла после команды
exit - выход'''.encode())
                    await writer.drain()
                    check=True
                    os.chdir('users_dir\\\\'+name)
                
                if check==False:
                    writer.write('Password is wrong! Try again'.encode())
                    await writer.drain()
                
    names.close()
    if nameflag==0:
        writer.write(r"Hello, stranger! What's your name?".encode())
        await writer.drain()
        name = await reader.read(100)
        writer.write("Hello, {0}! Create password!".format(str(name)[2:-1]).encode())
        await writer.drain()
        
        
        psw = await reader.read(100)
        names = open('names.txt','a')
        names.write(str([addr[0],str(name.decode()),str(psw)[2:-1]])+"\n")
        try:
            os.mkdir('users_dir\\\\'+name.decode())
            os.chdir('users_dir\\\\'+name.decode())
        except:
            os.mkdir('users_dir')
            os.mkdir('users_dir\\\\'+name.decode())
            os.chdir('users_dir\\\\'+name.decode())
        log=open('log.txt','w')
        log.close()
        writer.write('''Welcome to my server!
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat - отправляет содержимое файла,ввод имени файла после команды
mkdir - создает папку,ввод имени файла после команды
rmdir - удаляет пустую папку,ввод имени файла после команды
remove - удаляет файл,ввод имени файла после команды
rename - переименовывает,ввод имени файла после команды
copyto - копирует txt файл на сервер, ввод имени файла после команды
copyfrom - копирует txt файл с сервера, ввод имени файла после команды
exit - выход'''.encode())
        await writer.drain()
        
        names.close()
        check=True
    
    dirname = os.path.join(os.getcwd())   
    buffer_path=dirname[:dirname[:dirname.rfind('\\')].rfind('\\')]+'\\buffer'    
    while check==True:
        dirname = os.path.join(os.getcwd())
        data = await reader.read(100)
        message = data.decode()
        
        
    
        
        if message == 'exit':
            writer.close()
            print(f'OH NO! WE LOST {name} !!!')
            log=open('log.txt','a')
            log.write('exit\n')
            log.close()
        
        elif message == 'pwd':
            log=open('log.txt','a')
            log.write('pwd>>>'+dirname+'\n')
            log.close()
            writer.write(dirname.encode())
            await writer.drain()
            
        elif message == 'ls':
            ls='; '.join(os.listdir(dirname))
            if ls=='':
                ls='Папка пустая'
            log=open('log.txt','a')
            log.write('ls>>>'+ls+'\n')
            log.close()
            writer.write(ls.encode())
            await writer.drain()
            
        elif message == 'cat':
            writer.write("Enter name of file".encode())
            await writer.drain()
            data = await reader.read(100)
            cat_input = data.decode()
            try:
                cat = open(cat_input,'r')
                cat_output=[]
                for i in cat:
                    cat_output.append(i)
                if cat_output==[]:
                   writer.write('file is empty'.encode())
                   await writer.drain()
                   cat.close()
                   log=open('log.txt','a')
                   log.write('cat>>>'+'file is empty'+'\n')
                   log.close()
                else:    
                    writer.write((','.join(cat_output)).encode())
                    await writer.drain()
                    cat.close()
                    
                    log=open('log.txt','a')
                    log.write('cat>>>"'+(','.join(cat_output))+'"\n')
                    log.close()
            except:
                writer.write('there is no such file'.encode())
                await writer.drain()
                
                log=open('log.txt','a')
                log.write('cat>>>'+'there is no such file'+'\n')
                log.close()
                
            
        elif message=='mkdir':
            writer.write("Enter name of file".encode())
            await writer.drain()
            data = await reader.read(100)
            mkdir_path = data.decode()
            os.mkdir(mkdir_path)
            log=open('log.txt','a')
            log.write('mkdir>>>'+mkdir_path+'\n')
            log.close()
            writer.write('this message is never going to be printed'.encode())
            await writer.drain()
            
        elif message=='rmdir':
            writer.write("Enter name of file".encode())
            await writer.drain()
            data = await reader.read(100)
            rmdir_path = data.decode()
            try:
                os.rmdir(rmdir_path)
                writer.write('this message is never going to be printed'.encode())
                await writer.drain()
                log=open('log.txt','a')
                log.write('rmdir>>>'+rmdir_path+'\n')
                log.close()
            except:
                log=open('log.txt','a')
                log.write('rmdir>>>'+'there is no such file'+'\n')
                log.close()
                writer.write('there is no such file'.encode())
                await writer.drain()
                
        elif message=='remove':
            writer.write("Enter name of file".encode())
            await writer.drain()
            data = await reader.read(100)
            remove_path = data.decode()
            try:
                os.remove(remove_path)
                log=open('log.txt','a')
                log.write('remove>>>'+remove_path+'\n')
                log.close()
                writer.write('this message is never going to be printed'.encode())
                await writer.drain()
            except:
                log=open('log.txt','a')
                log.write('remove>>>'+'there is no such file'+'\n')
                log.close()
                writer.write('there is no such file'.encode())
                await writer.drain()
            
        elif message=='rename':
            writer.write("Enter name of file".encode())
            await writer.drain()
            data = await reader.read(100)
            rename_path_1 = data.decode()
            writer.write("Enter new name of file".encode())
            await writer.drain()
            data = await reader.read(100)
            rename_path_2 = data.decode()
            try:
                
                os.rename(rename_path_1,rename_path_2)
                log=open('log.txt','a')
                log.write('rename>>>'+rename_path_1+' to '+rename_path_2+'\n')
                log.close()
                writer.write('this message is never going to be printed'.encode())
                await writer.drain()
            except:
                log=open('log.txt','a')
                log.write('rename>>>'+'there is no such files'+'\n')
                log.close()
                writer.write('there is no such files'.encode())
                await writer.drain()
            
        elif message=='copyfrom':
            try:
                writer.write("Enter name of file".encode())
                await writer.drain()
                data = await reader.read(100)
                copy_source=buffer_path+'\\'+data.decode()
                f=open(data.decode(),'w')
                f.close()
                shutil.copy(copy_source,data.decode())
                writer.write('this message is never going to be printed'.encode())
                await writer.drain()
                log=open('log.txt','a')
                log.write('copyfrom>>>'+copy_source+'\n')
                log.close()
            except:
                writer.write('There is now such file'.encode())
                await writer.drain()
                log=open('log.txt','a')
                log.write('copyfrom>>>'+'there is no such files'+'\n')
                log.close()
        elif message=='copyto':
            try:
                writer.write("Enter name of file".encode())
                await writer.drain()
                data = await reader.read(100)
                copy_dist=buffer_path+'\\'+data.decode()
                f=open(copy_dist,'w')
                f.close()
                shutil.copy(data.decode(),copy_dist)
                writer.write('this message is never going to be printed'.encode())
                await writer.drain()
                log=open('log.txt','a')
                log.write('copyto>>>'+data.decode()+'\n')
                log.close()
            except:
                writer.write('There is now such file'.encode())
                await writer.drain()
                log=open('log.txt','a')
                log.write('copyto>>>'+'there is no such files'+'\n')
                log.close()
            
                
            
        else:
            writer.write('try again'.encode())
            await writer.drain()
            log=open('log.txt','a')
            log.write('try again'+'\n')
            log.close()
            
            
                   
          
async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 9095)
    
    ser = server.sockets[0].getsockname()
    print(f'Serving on {ser}')

    async with server:
        await server.serve_forever()


asyncio.run(main())