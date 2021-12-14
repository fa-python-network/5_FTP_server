HOST_ADDR = 'localhost'
PORT = 9108
INTERRUPT_MESSAGE = 'interrupting connection...'
HELP = '''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
mkdir <dirname> - создает папку с именем <dirname>
rmdir <dirname> - удаляет папку с именем <dirname>
rmfile <filename> - удаляет файл с именем <filename>
mv <source> <destination> - переименовывает файл
touch <filename> [Text] - создает файл с именем <filename> с текстом Text, если он указан
getfile <filename> - загружает файл filename с сервера
sendfile <filename> - отправляет файл filename на сервер
'''