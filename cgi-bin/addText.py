#!/usr/bin/env python3
import cgi, os
import html
import cgitb; cgitb.enable()
import sqlite3
import nltk
import time


def addInfo(filename):
	conn = sqlite3.connect('data/voc.db')
	c = conn.cursor()
	inpFile = open("data/" + filename, "rt")
		
	tokens = []
	for inputStr in inpFile:
		inputStr = inputStr.lower()
		tokens.extend(nltk.word_tokenize(inputStr))
	list_rm = []
	for i in tokens:
		if not i.isalpha():
			list_rm.append(i)				
	for i in list_rm:
		tokens.remove(i)
	tags = []
	tags.extend(nltk.pos_tag(tokens))
	inpFile.close()

	dic = dict.fromkeys(tags, 0)
	global amountW 
	amountW = len(tags)
	global amountUW
	amountUW = len(dic)
	for item in tags:
		dic[item] += 1
	
	c.execute('''SELECT name, id FROM tags''')
	sl = dict(c.fetchall())
	for item in dic:
		c.execute("SELECT COUNT(*) FROM voc WHERE word = '{0}' AND tagID = {1}".format(item[0], sl[item[1]]))
		t = c.fetchall()[0]
		if t[0] == 0:
			c.execute("INSERT INTO voc (word, amount, tagID) SELECT '{0}', {1}, '{2}' WHERE NOT EXISTS (SELECT * FROM voc WHERE word = '{0}' AND tagID = {2});".format(item[0], dic[item], sl[item[1]]))
		else:
			c.execute("UPDATE voc SET amount = amount + {2} WHERE word = '{0}' AND tagID = {1}".format(item[0], sl[item[1]], dic[item]))

	conn.commit()
	conn.close()

form_data = cgi.FieldStorage()
file_name = form_data["new_file"]

t1 = time.time()
if file_name.filename:
	fn = os.path.basename(file_name.filename)
	open("data/" + fn, 'wb').write(file_name.file.read())
	addInfo(fn)
t2 = time.time()
message ='<h2>Добавление нового текста прошло успешно.</h2><b><h3>Информация о пополнении словаря:</h3></b> \
	<table>\
	<tr><td><b>Имя файла с добавленным текстом:   </b></td> <td>{0}</td></tr>\
	<tr><td><b>Кол-во добавленных слов:    </b></td> <td>{1}</td></tr>\
	<tr><td><b>В том числе уникальных:    </b></td> <td> {2}</td></tr>\
	<tr><td><b>Время добавления:    </b></td> <td> {3:.4f} сек.</td></tr>\
	</table><br>Это окно закроется через 5 секунд автоматически.<br>'.format(file_name.filename, amountW, amountUW, t2 - t1)


print ("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<meta HTTP-EQUIV="REFRESH" CONTENT="5; URL=voc.py">
		<title>Добавление нового текста в словарь</title>
	</head>
	<body>""")
print(message)
print('''<br><center><a href="/cgi-bin/voc.py">[Закрыть отчет]</a></center>''')
print("""</body>
	</html>""")

