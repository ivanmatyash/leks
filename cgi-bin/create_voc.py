#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import time

form = cgi.FieldStorage()
file_name = form["filename"]

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<meta HTTP-EQUIV="REFRESH" CONTENT="5; URL=/cgi-bin/voc.py">
		<title>Создание нового словаря</title>
	</head>
	<body>""")
t1 = time.clock()
if file_name.filename:
	fn = os.path.basename(file_name.filename)
	open("data/" + fn, 'wb').write(file_name.file.read())
	global res 
	res = edit_text.makeVoc(fn)
t2 = time.clock()
res_time = t2 - t1
message ='<h2>Словарь успешно создан.</h2><b><h3>Информация о созданном словаре:</h3></b> \
	<table>\
	<tr><td><b>Имя файла: </b></td> <td>{0}</td></tr>\
	<tr><td><b>Слов добавлено: </b></td> <td>{1}</td></tr>\
	<tr><td><b>Время создания: </b></td> <td> {2:.4f} сек.</td></tr>\
	</table>Через 5 секунд вы будете перенаправлены на страницу со словарём.<br>'.format(file_name.filename, res, res_time)

print(message)
print('''<br><center><a href="/cgi-bin/voc.py">[Перейти к словарю]</a></center>''')
print("""</body>
	</html>""")
