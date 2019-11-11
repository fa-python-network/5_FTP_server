import socket
import os
import subprocess
"""

"pwd" = current dir
"ls" = show files
"cat fname" = show file with name = fname

"""

sock = socket.socket()

port = 1000

while True:
    try:
        sock.bind(("", port))
        sock.listen()
        print("SERVER ON PORT", port)
        break
    except:
        port+=1

subprocess.call(["mkdir", "SERVER_MAIN_FOLDER"])

dame = os.getcwd()

unknown = len(dame)

dirname = dame+"/SERVER_MAIN_FOLDER"



def requ(requesto):
    global dirname
    print("request =", requesto, '\n')

    if requesto == "pwd":
        abso = os.getcwd()
        if len(abso) == unknown:
            ans = abso +"/SERVER_MAIN_FOLDER"
        else:
            ans = abso        
        return ans[unknown:]


    elif requesto == "ls":
        #print(f"about to print the {dirname} contents")
        raw = os.listdir(dirname)
        
        i = 0
        while True:
            limit = len(raw)
            # print("AAAAAAAAAAAAAAAAAAAAAAAA", limit)
            # print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", i)
            if i >= limit:
                break
            if raw[i][0] == '.':
                del raw[i]
                i-=1
            i+=1

        ans = "\n".join(raw)

        if ans =="":
            return "empty folder."
        else:
            return ans
        

    elif requesto[0:3] == "cat":
        finame = requesto.split()[1]
        ans = subprocess.check_output(["cat", os.getcwd()
            +"/SERVER_MAIN_FOLDER"+"/"+finame]).decode()
        #print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR", ans)
        if ans =="":
            return "empty file."
        else:
            return ans

    elif requesto[0:5] == "mkdir":
        dname = requesto.split()[1]
        subprocess.call(["mkdir", os.getcwd()+"/SERVER_MAIN_FOLDER"+"/"+dname])
        #print(f'folder with name "{dname}" created successfully.\n')
        return f'folder with name "{dname}" created successfully.'

    elif requesto[0:2] == "cd":
        diname = requesto.split()[1]
        #print('OOOOOOOOOOOOOOOOOOOOOO', diname)
        #print("dirname =", dirname)
        if diname == ".." and dirname == "/root/aaa/5_FTP_server/SERVER_MAIN_FOLDER":
            return "NEIN, NO ACCESS"
        elif diname == "..":

            os.chdir("..")
        #subprocess.call(["cd", dirname+'/'+diname])
        else:
            os.chdir(dirname+'/'+diname)
        dirname = os.getcwd()
        #print(f'moved to folder with name "{diname}" successfully.\n')
        return f'moved to folder with name "{diname}" successfully.\n'

    elif requesto[0:4] == "copy":
        fodname = os.getcwd()+"/SERVER_MAIN_FOLDER"+"/"+requesto.split()[1]
        #print("==============================", fodname)
        destination = os.getcwd()+"/SERVER_MAIN_FOLDER"+"/" + requesto.split()[2]+"/"
        #print("==============================", destination)
        subprocess.call(["cp", fodname, destination])
        #print(f'folder or file with name "{fodname}" copied successfully.\n')
        return f'folder or file with name "{fodname}" copied successfully.'

    elif requesto[0:6] == "create":
        fodname = os.getcwd()+"/SERVER_MAIN_FOLDER"+"/"+requesto.split()[1]
        conts = ""
        try:
            conts = requesto.split()
            print(conts)
            del conts[0]
            del conts[0]
            res = " ".join(conts)
            print("RRRRRRRRRRREEEEEEEEEEEEDDDDDDDDDDDDSSSS", res)
        except:
            pass    
        #print("==============================", fodname)
        subprocess.call(["touch", fodname])

        print(fodname)

        f = open(fodname, 'w')

        f.write(res)

        f.close()      

        return f'file created successfully.'

    elif requesto[0:6] == "rename":
        fodname = os.getcwd()+"/SERVER_MAIN_FOLDER"+"/"+requesto.split()[1]
        #print("==============================", fodname)
        destination = os.getcwd()+"/SERVER_MAIN_FOLDER"+"/" + requesto.split()[2]
        #print("==============================", destination)
        subprocess.call(["mv", fodname, destination])
        #print(f'folder or file with name "{fodname}" copied successfully.\n')
        return f'file renamed successfully.'

    elif requesto[0:6] == "delete":
        fodname = requesto.split()[1]
        #print("==============================", fodname)
        subprocess.call(["rm","-rf", os.getcwd()+"/SERVER_MAIN_FOLDER"+"/"+fodname])
        #print(f'folder or file with name "{fodname}" deleted successfully.\n')
        return f'folder or file with name "{fodname}" deleted successfully.'

    elif requesto == "exit":
        return "BREAKFLAG"

    else:
        return "bad requesttt!!!!!!!!!"
    
    return


while True:
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()

    ans = requ(request)

    if ans == "BREAKFLAG":
        conn.send("EXITING...".encode())
        conn.close()
    # print("answer to request =", ans)
    else:
        response = conn.send(ans.encode())
    