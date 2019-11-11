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

def read_file(filename):
    try:
        file = open(filename)
        text = file.read()
        file.close()
        return text
    except:
        return 'there is no such file'


class Potoc(threading.Thread):

    def __init__(self,conn,addr):
        super().__init__()
        self.conn = conn
        self.addr = addr

    def run(self):

        self.dirname = os.path.join(os.getcwd(), 'docs')

        while True:
            req = recv_msg(self.conn)
            

            if req:
                logging.info('Request: ' + str(req))
                print(req)

                if req == 'pwd':
                    send_msg(self.conn,self.dirname)

                elif req == 'ls':
                     send_msg(self.conn, '; '.join(os.listdir(self.dirname)))

                elif 'exit' in req:
                    self.conn.close()

                elif req.strip()[:5] == 'mkdir':
                    new_dir = os.path.join(self.dirname, req.strip()[6:])
                    if os.path.isdir(new_dir) == False:
                        os.mkdir(new_dir)
                        send_msg(self.conn, 'dir is created')
                    else:
                        send_msg(self.conn, 'you cant create what has been created already')

                elif req.strip()[:5] == 'rmdir':
                    del_dir = os.path.join(self.dirname, req.strip()[6:])
                    if os.path.isdir(del_dir) == False:
                        send_msg(self.conn, 'you cant delete what does not exist, silly')
                    else:
                        os.rmdir(del_dir)
                        send_msg(self.conn, str(del_dir) + ' is removed, my lord')

                elif req.strip()[:6] == 'rename':
                    old_name = os.path.join(self.dirname, req.split(' ')[1])
                    new_name = os.path.join(self.dirname, req.split(' ')[2])
                    if os.path.isdir(os.path.join(self.dirname,old_name)) == True:
                        os.rename(old_name, new_name)
                        send_msg(self.conn,'it is renamed')
                    else:
                        send_msg(self.conn, 'there is no such directory ' + str(old_name))

                elif req.strip()[:6] == 'rmfile':
                    del_file = os.path.join(self.dirname, req.strip()[7:])
                    if os.path.isfile(del_file) == True:
                        os.remove(del_file)
                        send_msg(self.conn, str(del_file) + ' is removed')
                    else:
                        send_msg('there is no such file')

                else:
                    logging.info('Bad request')
                    send_msg(self.conn, 'bad request')

            elif req is None:
                break

            else: 
                logging.info('Bad request')
                send_msg(self.conn, 'bad request')

sock = socket.socket()

port = 6666             # проверка порта на занятость
while port!=65525:
    try:
        sock.bind(('',port))
        logging.info('ON')
        print('The port is {}'.format(port))
        break
    except:
        print('The port {} is not available. Checking new one...'.format(port))
        port+=1

sock.listen(1)
logging.info('Listening')
sock.setblocking(1)


while True:
    conn, addr = sock.accept()
    logging.info('Connected')

    Potoc(conn,addr).start()
    logging.info('Connected')

#logging.info("Closed")
#conn.close()