#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import edit_text
import sqlite3
import nltk



def addInfo(word, tag):
	word = word.lower()
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())
	
	c.execute("SELECT COUNT(*) FROM voc WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag]))
	t = c.fetchall()[0]
	if t[0] == 0:
		c.execute("INSERT INTO voc (word, amount, tagID) SELECT '{0}', {1}, '{2}' WHERE NOT EXISTS (SELECT * FROM voc WHERE word = '{0}' AND tagID = {2});".format(word, 1, sl[tag]))
	else:
		c.execute("UPDATE voc SET amount = amount + 1 WHERE word = '{0}' AND tagID = {1}".format(word, sl[tag]))

	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
word = form_data.getfirst("word", "-1")
tag = form_data.getfirst("tag", "-1")


message ='Вы находитесь на странице редактирования слова "{0}" с тегом "{1}".'.format(word, tag)

if word != '-1' and tag != '-1':
	pass
else:
	message = "Произошла ошибка передачи данных от клиента к серверу."

print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Изменение слова в словаре</title>
	</head>
	<body>""")
print(message)
print('<br><a href = "/cgi-bin/voc.py">Назад к словарю</a>')
print("""</body>
	</html>""")
