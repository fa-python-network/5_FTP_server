import socket

host = "localhost"

port = 1000

while True:
    request = input("vvedi zapros: \n")

    sock = socket.socket()
    while True:
    	try:
    		sock.connect((host, port))
    		break
    	except:
    		port+=1
    sock.send(request.encode())

    response = sock.recv(1024).decode()
    if response == "EXITING...":
    	break
    print()
    print("server's response =")
    print('"')
    print(response)
    print('"')
    print()

    sock.close()