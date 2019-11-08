import socket, os

'''
	pwd - current directory
	ls - list of files
	cat - file content
	exit - exit from client
	clear or cls - clear console window
'''


HOST = 'localhost'
PORT = 6666

try:
	os.system('clear')
	os.system('cls')
except:
	pass
print('*****************************************************************\n')
print('*  FTP-EMULATOR КЛИЕНТ. РАБОТА С ФАЙЛАМИ НА УДАЛЕННОМ СЕРВЕРЕ.  *\n')
print('*****************************************************************\n')
print('*  ОБРАТИТЕ ВНИМАНИЕ НА ДВЕ УДОБНЫЕ КОМАНДЫ:                    *\n')
print('*  clear/cls - очистить окно консоли, exit - выйти              *\n')
print('*****************************************************************\n')
print('\n\n\n')

while True:
	request = input('>')
	
	if request == 'exit':
		print('Клиент закрыт')
		break
	
	elif request == 'clear':
		try:
			os.system('clear')
			os.system('cls')
		except:
			pass
	
	else:
		sock = socket.socket()
		sock.connect((HOST, PORT))
		
		sock.send(request.encode())
		
		response = sock.recv(1024).decode()
		print(response)
		
		sock.close()