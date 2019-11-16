from datetime import datetime


class Logfile(object):

    def __init__(self, file_name = "file.log"):
        self.file_name = file_name
        

    def write_to_file(self, data: str, file_name = None):
        

        if file_name is None:
            server = "server"
            file_name = self.file_name
    
        with open(file_name, "a", encoding="utf-8") as f:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {data}", file=f)

    def serverstart(self,l):
        self.write_to_file(f"{l} was connected  ", "connection.log")

    def serverend(self,l):  
        self.write_to_file(f"{l} was disconnected  ", "connection.log")
    
    def mkdir(self,obj):
        self.write_to_file(f"{obj} was created  ", "operation.log")
    def rm(self,obj):
        self.write_to_file(f"{obj} was deleted  ", "operation.log")
    
    def delete(self,obj):
        self.write_to_file(f"{obj}  was deleted  ", "operation.log")
    
    def rename(self,old,new):
        self.write_to_file(f"{old} object was renamed to {new} ","operation.log")

    def copyfromclienttoserver(self,file):
        self.write_to_file(f"{file}  was sent from client to server  ","operation.log")

    def copyfromservertoclient(self,file):
        self.write_to_file(f"{file}  was sent from  server to client  ","operation.log")

    


