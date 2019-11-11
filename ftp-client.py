import socket

HOST = 'localhost'

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

while True:
	PORT = input('Your port: ')
	if 1024<int(PORT)<=65525:
		print('good')
		break
	else:
		print('try another port')

while True:
    request = input('>')
    
    sock = socket.socket()
    sock.connect((HOST, int(PORT)))
    
    if 'exit' in request:
    	send_msg(sock, request)
    	sock.close()
    	break 

    send_msg(sock, request)
    
    response = recv_msg(sock)
    print(response)
    
    sock.close()