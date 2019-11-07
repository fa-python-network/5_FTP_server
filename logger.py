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

    def serverstart(self):
        self.write_to_file("Connection was started  ")

    def serverend(self):  
        self.write_to_file("Connection was stopped  ")
    
    def mkdir(self,obj):
        self.write_to_file(f"{obj} was created  ")
    def rm(self,obj):
        self.write_to_file(f"{obj} was deleted  ")
    
    def delete(self,obj):
        self.write_to_file(f"{obj}  was deleted  ")
    
    def rename(self,old,new):
        self.write_to_file(f"{old} object was renamed to {new} ")

    def copyfromclienttoserver(self,file):
        self.write_to_file(f"{file}  was sent from client to server  ")

    def copyfromservertoclient(self,file):
        self.write_to_file(f"{file}  was sent from  server to client  ")

    


