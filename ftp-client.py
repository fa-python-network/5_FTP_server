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
exit - закрыть клиент
clear - очистить окно консоли
help - открыть помощь
''')

	else:
		sock = socket.socket()
		sock.connect((HOST, PORT))

		sock.send(request.encode())

		response = sock.recv(1024).decode()
		print(response)

		sock.close()
