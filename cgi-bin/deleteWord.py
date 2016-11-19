#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3
import nltk



def removeInfo(word, tag):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())

	c.execute("DELETE FROM voc WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag]))
	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
word = form_data.getfirst("word", "-1")
tag = form_data.getfirst("tag", "-1")

message ='Слово "{0}" с тегом "{1}" успешно удалено из словаря. Сейчас вы будете перенаправлены.'.format(word, tag)

if word != '-1' and tag != '-1':
	removeInfo(word, tag)
else:
	message = "Произошла ошибка передачи данных от клиента к серверу, сейчас вы будете перенаправлены."

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<meta HTTP-EQUIV="REFRESH" CONTENT="3; URL=/cgi-bin/voc.py">
		<title>Удаление слова из словаря</title>
	</head>
	<body>""")
print(message)
print('<br><a href = "/cgi-bin/voc.py">Назад к словарю</a>')
print("""</body>
	</html>""")
