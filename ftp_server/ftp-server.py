import socket
import os
import shutil
'''
pwd                                 - показывает название рабочей директории
ls                                  - показывает содержимое текущей директории
mkdir <foldername>                  - создает папку
rmdir <foldername>                  - удаляет папку
rm <filename>                       - удаляет файл
rename <oldfilename> <newfilename>  - переименовывает файл
exit                                - закрытие клиента
send <filename>                     - переносит файл с клиента на сервер
copy <filename>                     - переносит файл с сервера на клиент
'''

dirname = os.path.join(os.getcwd(), 'docs')
dirname1 = os.path.join(os.getcwd(), 'docs_from')

def file_name_check(name):

    try:

        name = name.split('.')
        name = name[0] + '.' + name[1]
        return True

    except IndexError:

        return False


def process(req):

    r=req.split(' ')

    if r[0] == 'pwd':

        return dirname

    elif r[0] == 'ls':

        return '; '.join(os.listdir(dirname))

    elif r[0] == 'mkdir':

        try:

            folder_name = r[1]
            path = os.path.join(dirname, folder_name)

            try:

                os.mkdir(path)
                return 'Папка {0} успешно создана'.format(str(folder_name))

            except FileExistsError:

                return 'Такая папка уже существует по этому пути {0}'.format(str(path))

        except IndexError:

            return 'Вы не назвали папку'

    elif r[0] == 'rmdir':

        try:

            folder_name = r[1]
            path = os.path.join(dirname, folder_name)

            try:

                shutil.rmtree(path)
                return 'Папка {0} успешно удалена'.format(str(folder_name))

            except FileNotFoundError:

                return 'Такой папки не существует по этому пути {0}'.format(str(path))

        except IndexError:

            return 'Вы не назвали папку'

    elif r[0] == 'rm':

        try:

            file_name = r[1]

            if file_name_check(file_name) is False:
                return 'Не указано расширение файла'

            path = os.path.join(dirname, file_name)

            try:

                os.remove(path)
                return 'Файл {0} успешно удален'.format(str(file_name))

            except FileNotFoundError:

                return 'Такого файла не существует по этому пути {0}'.format(str(path))

        except IndexError:

            return 'Вы не назвали файл'

    elif r[0] == 'rename':

        try:

            old_file_name = r[1]

            try:

                new_file_name = r[2]

                if file_name_check(old_file_name) is False:
                    return 'Не указано расширение файла'
                if file_name_check(new_file_name) is False:
                    return 'Не указано расширение файла'

                path1 = os.path.join(dirname, old_file_name)
                path2 = os.path.join(dirname, new_file_name)

                try:

                    os.rename(path1, path2)
                    return 'Файл {0} успешно переименован в {1}'.format(old_file_name, new_file_name)

                except FileNotFoundError:

                    return 'Такого файла не существует по этому пути {0}'.format(str(path))

            except IndexError:

                return 'Вы не дали новое название файлу'

        except IndexError:

            return 'Вы не указали название файла'

    elif r[0] == 'exit':

        os.abort()

    elif r[0] == 'send':

        try:

            s_file = r[1]
            path_to = os.path.join(dirname, s_file)
            path_from = os.path.join(dirname1, s_file)
            if file_name_check(s_file) is False:
                return 'Не указано расширение файла'

            try:

                file_from = open(path_from, 'r')
                file_to = open(path_to, 'w')
                text = file_from.readlines()
                print(text)
                file_to.writelines(text)
                file_to.close()
                file_from.close()

                return 'Файл {0} успешно перенесен'.format(s_file)



            except FileNotFoundError:

                return 'Такого файла не существует по этому пути {0}'.format(str(path_from))



        except IndexError:

            return 'Вы не указали название файла'

    elif r[0] == 'copy':

        try:

            s_file = r[1]
            path_to = os.path.join(dirname1, s_file)
            path_from = os.path.join(dirname, s_file)
            if file_name_check(s_file) is False:
                return 'Не указано расширение файла'

            try:

                file_from = open(path_from, 'r')
                file_to = open(path_to, 'w')
                text = file_from.readlines()
                print(text)
                file_to.writelines(text)
                file_to.close()
                file_from.close()

                return 'Файл {0} успешно перенесен'.format(s_file)



            except FileNotFoundError:

                return 'Такого файла не существует по этому пути {0}'.format(str(path_from))



        except IndexError:

            return 'Вы не указали название файла'


    return 'bad request'


PORT = 9090

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())

conn.close()
