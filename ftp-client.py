import socket

sock = socket.socket()
sock.setblocking(1)

host = input("Введите адрес хоста или lh: ")
if host == "lh":
	host = 'localhost'
else:
	host_ls = host.split(".", 4)
	for i in host_ls:
		if 0 <= int(i) <= 255:
			pass
		else:
			host = 'localhost'
port = int(input("Введите адрес порта: "))
if 1024 <= int(port) <= 65535:
	pass

sock.connect((host, port))
print('Введите Ваше сообщение/запрос или "exit" для выхода: ')
msg = ""

while True:
	request = input('>').strip()
	if request == "exit":
		a = 1
		break
	sock.send(request.encode())
	response = sock.recv(1024).decode()
	msg += request + ' '
	print (response)

if (a == 1) and (msg == ''):
	print('Disconnecting...')
	sock.close()
else:
	print('Disconnecting...')
	sock.close()
	print("Вы ввели: ", msg)