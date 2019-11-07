import socket
import os
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <dirname>- создает директорию
rmdir <dirname>-удаляет директорию
remove <filename> - отправляет содержимое файла
rename <filename>- переименовывает файл
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req== 'cat filik':
        #file_name='filik.txt'
        f=open(path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'filik.txt'))
        line=f.readline()
        spisok_strok=[]
        while line:
            spisok_strok.append(line)
            line=f.readline()
        f.close() 
        return ' '.join(spisok_strok)
    elif req == 'mkdir my_dir':
        return os.mkdir('my_dir')
    elif req == 'rmdir my_dir':
        return shutil.rmtree('my_dir')
    elif req == 'remove filik':
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'filik.txt')
        return os.remove(path)
    elif req=='rename filik':
        return os.rename('filik.txt','my_file.txt')
    else:
        return 'Может Вы ошиблись?'
        
PORT = 9098
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

while True:
    print("Прослушиваю порт: ", PORT)
    conn, addr = sock.accept()
    print(addr)
    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    if (request=='pwd') or (request=='ls') or (request=='cat filik'):
        conn.send(response.encode())
    elif (request=='mkdir my_dir') or (request == 'rmdir my_dir') or (request == 'remove filik') or (request == 'rename filik'):
        conn.send('Я сделал, как Вы просили.(Сервер)'.encode())
    else:
        conn.send(response.encode())
conn.close()
input()
