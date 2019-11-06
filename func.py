import socket
import os
import ftplib
from logger import Logfile
'''
pwd - показывает название рабочей директории
ls  - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
ls f - показывает содержимое 
mkdir <filename> - создание папки в текущей директории
rm <filename> - удалеяет папкy в текущей директории
delete <filename> - удаляет файл в текущей директории
rename <filename> <new name> - переименовывает файл/директорию в <new name>
exit - отключение клиента от сервера
copy.from.client - cкопировать файл с клиента на сервер
co[y.from.server -
'''

dirname = os.getcwd()

def process(r):
    l=Logfile()
    req=r.split()
    if req[0] == 'pwd':
        return dirname

    elif req[0] == 'ls':
        return '; '.join(os.listdir(dirname))

    elif req[0] == 'ls f':
        pass

    elif req[0] == 'mkdir':
        try:
            path=str(os.getcwd())+'/'+req[1]
            #print(path)
        
            try:
                os.mkdir(path)
                p=path+' has been created'
                l.mkdir(req[1])
                return p
            except FileExistsError:
                return 'This path is already existed'
        except IndexError:
            return 'Вы не ввели название папки'

    elif req[0]== 'rm':
        try:
            try:
                path= os.path.abspath(req[1])
                os.rmdir(path,  dir_fd=None)
                l.rm(req[1])
                return 'The directory has been deleted'
            except FileNotFoundError:
                return 'No such file or directory'
            
        except IndexError:
            return 'Вы не ввели название папки'
    
    elif req[0] == 'delete':
        try:
            try:
                path= os.path.abspath(req[1])
                os.remove(path, dir_fd = None)
                l.delete(req[1])
                return 'The file has been deleted'
            except FileNotFoundError:
                return 'No such file or directory'
            
        except IndexError:
            return 'Вы не ввели название файла'
    
    elif req[0] == 'rename':
        try:
                try:
                    path= os.path.abspath(req[1])
                    try:
                         os.rename(req[1], req[2], src_dir_fd=None, dst_dir_fd=None)
                         l.rename(req[1],req[2])
                         return 'The name has been changed'
                    except IndexError:
                        return 'Вы не ввели новое название'
                except FileNotFoundError:
                    return 'No such file or directory'


        except IndexError:
            return 'Вы не ввели название файла'
    
    elif req[0] == 'exit':
        l.serverend()
        return 'Disconnected'


    ''' на стадии доработки
    elif req[0] == 'copy.from.client':
        host = "localhost"
        filename = req[1]
        con = ftplib.FTP(host)
        con.login()
        f = open(filename, "rb")
        send = con.storbinary("STOR "+ filename, f)
        con.close
    '''

    return 'Inappropriate request'