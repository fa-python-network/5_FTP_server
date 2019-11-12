import socket
import os
import shutil
import datetime

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
'''

dirname = os.path.join(os.getcwd(), 'docs')
dirlevel = 0

def process(req):
	global conn
	global dirname																									#текущая папка
	global dirlevel																									#уровень в файловой системе, чтобы не вылезти из дозволенных границ
	req = req + ' _eoc_'																							#флаг окончания команды
	if req.split(' ')[0] == 'pwd':																					#текущая директория
		if not dirname.split('docs')[1]:
			return '\\'
		return dirname.split('docs')[1]

	elif req.split(' ')[0] == 'ls':																					#список файлов
		return '; '.join(os.listdir(dirname))

	elif req.split(' ')[0] == 'cat':																				#содержимое файла
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if os.path.isfile(os.path.join(dirname,req.split(' ')[1])):
					if '..' in req.split(' ')[1]:
						return 'Not allowed using .. in complex path!'
					with open(os.path.join(dirname,req.split(' ')[1]),'r',encoding='UTF-8') as f:
						return f.read()
				else:
					return 'This is not a file!'
			else:
				return 'no such file'
		else:
			return 'empty filename'

	elif req.split(' ')[0] == 'mkdir':																				#создание папки
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				return 'dir (file) already exists!'
			else:
				if '..' in req.split(' ')[1]:
					return 'Not allowed using .. in complex path!'
				os.mkdir(os.path.join(dirname,req.split(' ')[1]),777)
				return f'Dir is created!'
		else:
			return 'no filename'

	elif req.split(' ')[0] == 'rm':																					#удаление файла или папки
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if '..' in req.split(' ')[1]:
					return 'Not allowed using .. in complex path!'
				if os.path.isfile(os.path.join(dirname,req.split(' ')[1])):
					os.remove(os.path.join(dirname,req.split(' ')[1]))
				else:
					shutil.rmtree(os.path.join(dirname,req.split(' ')[1]))
				return 'file/directory deleted!'
			else:
				return 'no such file or directory!'
		else:
			return 'no filename or dirname'


	elif req.split(' ')[0] == 'touch':																					#создать файл (пустой или с содержимым)
		if req.split(' ')[1] != '_eoc_':
			if not os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if '..' in req.split(' ')[1]:
					return 'Not allowed using .. in complex path!'
				if req.split(' ')[2] == '_eoc_':
					with open(os.path.join(dirname,req.split(' ')[1]),'w') as f:
						f.write('');
				else:
					with open(os.path.join(dirname,req.split(' ')[1]),'w') as f:
						f.write('');
					with open(os.path.join(dirname,req.split(' ')[1]),'a') as f:
						for word in range(2,len(req.split(' '))-1):
							f.write(req.split(' ')[word]+' ');

				return 'file created!'
			else:
				return 'File already exists!'
		else:
			return 'filename required!'

	elif req.split(' ')[0] == 'rename':																					#переименовать файл или папку
		if req.split(' ')[1] != '_eoc_' and req.split(' ')[2] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if '..' in req.split(' ')[1] or '..' in req.split(' ')[2]:
					return 'Not allowed using .. in complex path!'
				os.rename(os.path.join(dirname,req.split(' ')[1]),os.path.join(dirname,req.split(' ')[2]))
				return 'rename done!'
			else:
				return 'First file/folder does not exist!'
		else:
			return 'filename (x2) required!'


	elif req.split(' ')[0] == 'cp':																					#копировать файл или папку
		if req.split(' ')[1] != '_eoc_' and req.split(' ')[2] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if '..' in req.split(' ')[1] or '..' in req.split(' ')[2]:
					return 'Not allowed using .. in complex path!'
				if os.path.isfile(os.path.join(dirname,req.split(' ')[1])):
					shutil.copy(os.path.join(dirname,req.split(' ')[1]),os.path.join(dirname,req.split(' ')[2]))
				else:
					shutil.copytree(os.path.join(dirname,req.split(' ')[1]),os.path.join(dirname,req.split(' ')[2]))
				return 'copy done!'
			else:
				return 'First file/folder does not exist!'



	elif req.split(' ')[0] == 'cd':																		#сменить текущий каталог (с защитой файлов родительской директории)
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if (os.path.isdir(os.path.join(dirname,req.split(' ')[1]))):
					if '..' in req.split(' ')[1] and req.split(' ')[1] != '..':
						return 'Not allowed using .. in complex path!'
					if req.split(' ')[1] == '.':
						return 'Done'
					if req.split(' ')[1] == '..':
						if dirlevel > 0:																#не находимся ли мы уже в корне пользовательской папки?
							dirlevel-=1
						else:
							return 'Not allowed!'
					dirname = os.path.join(dirname,req.split(' ')[1])
					if req.split(' ')[1] != '..':														#спустились на один уровень вниз
						dirlevel+=1
						return 'Done'
					else:
						return 'Done'
				else:
					return 'This is not a dir!'
			else:
				return 'Dir with such name does not exist!'
		else:
			return 'dir name required!'



	elif req.split(' ')[0] == 'get':																				#скачать текстовый файл
		if req.split(' ')[1] != '_eoc_':
			if os.path.exists(os.path.join(dirname,req.split(' ')[1])):
				if os.path.isfile(os.path.join(dirname,req.split(' ')[1])):
					if '..' in req.split(' ')[1]:
						return 'Not allowed using .. in complex path!'
					with open(os.path.join(dirname,req.split(' ')[1]),'r',encoding='UTF-8') as f:
						return 'success-!-!-!->'+f.read()
				else:
					return 'This is not a file!'
			else:
				return 'no such file'
		else:
			return 'empty filename'



	elif req.split(' ')[0] == 'push':																				#загрузить текстовый файл от клиента
		if req.split(' ')[1] != '_eoc_':
			if '..' in req.split(' ')[1] or '/' in req.split(' ')[1] or '\\' in req.split(' ')[1]:
				return 'Not allowed using .. \\ / in complex path!'
			filecontent = conn.recv(1024)
			with open(os.path.join(dirname,req.split(' ')[1]),'w') as f:
				f.write(filecontent.decode())
			return 'File uploaded!'



	return 'bad request'																							#неправильный запрос


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(5)

logfile = 'access.log'
print('Сервер запущен!')

while True:
	conn, addr = sock.accept()

	request = conn.recv(1024).decode()
	with open(logfile,'a') as f:
		f.write(datetime.datetime.today().strftime('%Y-%m-%d %H:%M')+' - '+request+'\n')

	response = process(request)
	conn.send(response.encode())

	conn.close()
