import socket
import os
import logging
import threading
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''
logging.basicConfig(filename="log.log", level = logging.INFO)
dirname = os.path.join(os.getcwd(), 'docs')

def send_msg(conn: socket.socket,msg):
    """
    отправка сообщений
    """
    header=len(msg)
    formated_msg = f'{header:<4}{msg}'.encode()
    conn.send(formated_msg)

def recv_msg(conn: socket.socket):
    """
    принятие сообщений
    """
    try:
        header=int(conn.recv(4).decode().strip())
        msg=conn.recv(2*header)
        return msg.decode()
    except:
        pass

def handle(conn,addr):
    """
    обработка сообщений
    """
    request = recv_msg(conn)
    logging.info('Request: ' + str(request))
    print(request)
    
    #if 'exit' in request:
     #   conn.close()
      #  return 'closed'

    response = process(request)
    logging.info('Response: ' + str(response))
    send_msg(conn, response)

def process(req):
    """
    обработка команд
    """
    global dirname

    if req == 'pwd':
        return dirname

    elif req == 'ls':
        return '; '.join(os.listdir(dirname))

    elif req == 'exit':
        logging.info('Disconnected')
        conn.close()
        return 'closed'

    elif req.strip()[:5] == 'mkdir':
        new_dir = os.path.join(dirname, req.strip()[6:])
        if os.path.isdir(new_dir) == False:
            os.mkdir(new_dir)
            return 'dir is created'
        else:
            return 'you cant create what has been created already'

    elif req.strip()[:5] == 'rmdir':
        del_dir = os.path.join(dirname, req.strip()[6:])
        if os.path.isdir(del_dir) == False:
            return 'you cant delete what does not exist, silly'
        else:
            os.rmdir(del_dir)
            return str(del_dir) + ' is removed, my lord'

    elif req.strip()[:6] == 'rename':
        old_name = os.path.join(dirname, req.split(' ')[1])
        new_name = os.path.join(dirname, req.split(' ')[2])
        if os.path.isdir(os.path.join(dirname,old_name)) == True:
            os.rename(old_name, new_name)
            return 'it is renamed'
        else:
            return 'there is no such directory ' + str(old_name)

    elif req.strip()[:6] == 'rmfile':
        del_file = os.path.join(dirname, req.strip()[7:])
        if os.path.isfile(del_file) == True:
            os.remove(del_file)
            return str(del_file) + ' is removed'
        else:
            return 'there is no such file'

    else:
        logging.info('Bad request')
        return 'bad request'

sock = socket.socket()

port = 6666             # проверка порта на занятость
while port!=65525:
    try:
        sock.bind(('',port))
        logging.info('ON')
        print('The port is {}'.format(port))
        break
    except:
        print('The port {} is not available. Checking new one...')
        port+=1

sock.listen(1)
logging.info('Listening')
sock.setblocking(1)

try:
    c = 0 
    while True:
        conn, addr = sock.accept()
        c+=1
        logging.info('Connected')

        tr = threading.Thread(target=handle, args=(conn,addr))
        logging.info('started potoc ' + str(c))
        print('potoc '+ str(c))
        tr.start()
finally:
    logging.info('Closed')
    conn.close()

#logging.info("Closed")
#conn.close()