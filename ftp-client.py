import socket, os	#работаем с сокетом + работа с модулем os для очистки экрана консоли

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


HOST = 'localhost'		#параметры подключения
PORT = 6666

try:
	os.system('clear')		#очистка окна консоли (кроссплатформенно)
	os.system('cls')
except:
	pass
print('*****************************************************************\n')		#приветствие
print('*  FTP-EMULATOR КЛИЕНТ. РАБОТА С ФАЙЛАМИ НА УДАЛЕННОМ СЕРВЕРЕ.  *\n')
print('*****************************************************************\n')
print('*  ОБРАТИТЕ ВНИМАНИЕ НА ДВЕ УДОБНЫЕ КОМАНДЫ:                    *\n')
print('*  clear - очистить окно консоли, exit - выйти, help - помощь   *\n')
print('*****************************************************************\n')
print('\n\n\n')

print('Введите логин:')		#получаем данные для входа. Они каждый раз отправляются на сервер как токены
login = input()
print('Введите пароль:')
password = input()

while True:		#постоянно получаем команды от пользователя
	request = input('>')

	if request == 'exit':		#выйти из клиента
		print('Клиент закрыт')
		break

	elif request == 'clear':		#очистить экран
		try:
			os.system('clear')
			os.system('cls')
		except:
			pass

	elif request == 'help':		#помощь
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

	else:		#а здесь команды, которые подразумевают отправку данных на сервер, то есть они не выполняются чисто локально как те, что были выше
		sock = socket.socket()
		sock.connect((HOST, PORT))

		sock.send(f'{login}->{password}'.encode())		#отправляем условный токен
		sansw = sock.recv(1024)
		if sansw.decode() == 'allowed!':		#если логин и пароль верные

			if request.split(' ')[0] == 'push':			#отдельная логика работы команды по отправке файла на сервер из текущей директории
				request+=' _eoc_'
				if request.split(' ')[1] != '_eoc_':		#проверка на наличие флага конца команды
					if '..' in request.split(' ')[1] or '/' in request.split(' ')[1] or '\\' in request.split(' ')[1]:		#защита от лазания по ФС
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

			else:		#если это остальные серверные команды

				sock.send(request.encode())

				response = sock.recv(1024).decode()

				if request.split(' ')[0] == 'get':		#корректив для команды по получению файла с удаленного сервера
					if response.split('-!-!-!->')[0] == 'success':
						with open(request.split(' ')[1],'w') as f:
							f.write(response.split('-!-!-!->')[1])
						print('File got! Check your working directory!')
					else:
						print(response)

				else:
					print(response)

		else:
			print('Invalid login or password! Restart your client and enter valid data!')		#если логин или пароль ошибочные

		sock.close()		#после каждой команды рвем соединение
