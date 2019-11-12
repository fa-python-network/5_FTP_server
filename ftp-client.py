import socket, os

'''
	pwd 								- текущая директория
	ls 									- список файлов
	cat <filename> 						- содержимое файла
	mkdir <dirname> 					- создать папку
	touch <name> [content] 				- создать файл с содержимым content
	rm <file or dir name>				- удалить файл или папку с вложениями
	rename <f/d name> <f/d name>		- переименовать файл, папку с первым названием
	cp <f/d name> <f/d name>			- копировать файл, папку с первым названием
	cd <dirname>						- перейти в папку dirname
	get <filename>						- скачать с сервера файл
	push <filename>						- загрузить на сервер файл
	exit 								- закрыть клиент
	clear 								- очистить окно консоли
	help 								- открыть помощь
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
print('*  clear - очистить окно консоли, exit - выйти, help - помощь   *\n')
print('*****************************************************************\n')
print('\n\n\n')

print('Введите логин:')
login = input()
print('Введите пароль:')
password = input()

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

	elif request == 'help':
		print('''
pwd - текущая директория
ls  - список файлов
cat <filename> - содержимое файла
mkdir <dirname> - создать папку
touch <name> [content] - создать файл с содержимым content
rm <file or dir name> - удалить файл или папку с вложениями
rename <f/d name> <f/d name> - переименовать файл, папку с первым названием
cp <f/d name> <f/d name> - копировать файл, папку с первым названием
cd <dirname> - перейти в папку dirname
get <filename> - скачать с сервера файл
push <filename> - загрузить на сервер файл
exit - закрыть клиент
clear - очистить окно консоли
help - открыть помощь
''')

	else:
		sock = socket.socket()
		sock.connect((HOST, PORT))
		
		sock.send(f'{login}->{password}'.encode())
		sansw = sock.recv(1024)
		if sansw.decode() == 'allowed!':

			if request.split(' ')[0] == 'push':
				request+=' _eoc_'
				if request.split(' ')[1] != '_eoc_':
					if '..' in request.split(' ')[1] or '/' in request.split(' ')[1] or '\\' in request.split(' ')[1]:
						print('Not allowed using .. / \\ in complex path!')
					else:
						if os.path.exists(request.split(' ')[1]):
							if os.path.isfile(request.split(' ')[1]):
								sock.send(request.encode())
								with open(request.split(' ')[1],'r') as f:
									forsend = f.read().encode()
								sock.send(forsend)
								answer = sock.recv(1024)
								print(answer.decode())
							else:
								print('This is not a file!')
						else:
							print('file does not exist!')
				else:
					print('filename required!')

			else:

				sock.send(request.encode())

				response = sock.recv(1024).decode()
				if request.split(' ')[0] == 'get':
					if response.split('-!-!-!->')[0] == 'success':
						with open(request.split(' ')[1],'w') as f:
							f.write(response.split('-!-!-!->')[1])
						print('File got! Check your working directory!')
					else:
						print(response)

				else:
					print(response)
					
		else:
			print('Invalid login or password! Restart your client and enter valid data!')

		sock.close()
